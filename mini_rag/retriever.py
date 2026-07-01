# ##############################################################################
# File: retriever.py
# Purpose: Retrieval primitives and agent-facing wrappers. The retrieve()
#          function is the single retrieval surface that both the agent's
#          search_knowledge tool and the eval script call. Production retrieval
#          behavior lives here; everything else is a presentation layer on top.
#
# Contents:
#   Constants:
#     _RRF_K                   - Reciprocal Rank Fusion constant
#     _FUSION_TOP              - Candidates pulled from each retriever for fusion
#     _WORD_RE                 - Hyphen-aware tokenizer regex
#     _PORTER                  - Porter stemmer singleton (snowballstemmer)
#
#   Module-private state:
#     _bm25                    - Lazy BM25 index singleton
#     _cross_encoder           - Lazy cross-encoder reranker singleton
#
#   Functions:
#     _default_tokenizer()     - Hyphen-split + Porter stem BM25 tokenizer (v6)
#     _get_bm25()              - Lazy-build BM25 index from chunks in Chroma
#     _get_cross_encoder()     - Lazy-load the cross-encoder reranker
#     retrieve()               - Hybrid retrieval + cross-encoder rerank
#     search_knowledge()       - Agent-facing wrapper; formats hits as text
#     list_sources()           - Summary of documents and chunk counts in store
# ##############################################################################


# Standard library
import re
from collections import Counter

# Third-party
import snowballstemmer
from langchain_core.documents import Document

# Local
from config import TOP_K, RERANK_TOP, CROSS_ENCODER_MODEL
from mini_rag import chroma_client
from mini_rag.utils import get_vector_store


# ##############################################################################
# Hybrid retrieval configuration
# ##############################################################################


# Reciprocal Rank Fusion constant. Standard value is 60; lower amplifies the
# weight of top ranks, higher smooths the fusion.
_RRF_K = 60

# How many candidates to pull from each retriever before fusion. Wider net
# catches more cross-retriever overlaps; narrower net is faster and less prone
# to BM25 false positives polluting the fused result.
_FUSION_TOP = 20


# ##############################################################################
# Reciprocal Rank Fusion
# ##############################################################################


def _rrf_fuse(
    dense_ranks: dict[str, int],
    bm25_ranks: dict[str, int],
    k: int = _RRF_K,
) -> dict[str, float]:
    """Combine two ranked lists via Reciprocal Rank Fusion.

    Args:
        dense_ranks (dict[str, int]): id -> 1-based rank from dense retrieval.
        bm25_ranks (dict[str, int]): id -> 1-based rank from BM25 retrieval.
        k (int): RRF constant; standard value is 60. Lower amplifies the
            weight of top ranks, higher smooths the fusion.

    Approach:
        Each id's score is the sum of `1 / (k + rank)` across both retrievers.
        Ids missing from a retriever contribute approximately zero from that
        side (their rank is treated as a very large number, so 1/(k+rank) tends to zero).

    Returns:
        dict[str, float]: id -> fused score. Sort descending for the
            ranked-fusion order.
    """
    all_ids = set(dense_ranks) | set(bm25_ranks)
    return {
        cid: (1.0 / (k + dense_ranks.get(cid, 1e9)))
        + (1.0 / (k + bm25_ranks.get(cid, 1e9)))
        for cid in all_ids
    }


# BM25 index singleton. Built lazily on first retrieve() call from chunks
# already in Chroma. Not shared with the ingestion pipeline since BM25 only
# matters at query time.
_bm25 = None

# Cross-encoder reranker singleton. Lazy-loaded on first retrieve() call.
# Reads (query, chunk) pairs with cross-attention and produces relevance
# scores. Slower than bi-encoder retrieval but much more precise; used only
# to rerank the top-RERANK_TOP candidates from the hybrid retrieval step.
_cross_encoder = None


# ##############################################################################
# BM25 index
# ##############################################################################


# BM25 tokenizer state. The hyphen-aware splitter and the Porter stemmer are
# module-level singletons so they're built once per process and reused on
# every chunk + query that goes through retrieval.
_WORD_RE = re.compile(r"\w+")
_PORTER = snowballstemmer.stemmer("porter")


def _default_tokenizer(text: str) -> list[str]:
    """Production BM25 tokenizer: hyphen-aware split + Porter stemming.

    Approach:
        Splits on any non-word character (whitespace, hyphens, punctuation)
        instead of whitespace only. This breaks compound names like
        "SARLO-80" into ["sarlo", "80"], so a query naming "SARLO" can
        match a chunk that contains only "SARLO-80". Then applies Porter
        stemming so morphological variants ("embedding" / "embeddings",
        "trained" / "training") collapse to the same token.

        Both transformations were measured against the v5 baseline in the
        ablation study at `tests/ablation/bm25_tokenization.py`. The
        combined variant lifted Recall@5 from 0.517 to 0.690 with no
        per-type regressions. See section 4.8 in DEVLOG.

    Args:
        text (str): Chunk or query text.

    Returns:
        list[str]: Tokens used for both BM25 corpus indexing and query
            scoring (the same tokenizer must run both sides).
    """
    return [_PORTER.stemWord(t) for t in _WORD_RE.findall(text.lower())]


def _get_bm25(tokenizer=_default_tokenizer):
    """Lazy-build the in-memory BM25 index from chunks already in Chroma.

    Args:
        tokenizer: Callable that takes a chunk's text and returns a list of
            tokens. Defaults to lowercase + whitespace split. Pass an
            alternate tokenizer to ablate stemming, stopwords, hyphenation,
            etc. Note: the cached singleton is built once per process; to
            rebuild under a different tokenizer (e.g. across ablation
            variants), clear `_bm25` first.

    Approach:
        On first call, pulls all chunk documents and ids out of the Chroma
        collection, tokenizes each chunk with the supplied tokenizer, and
        constructs a BM25Okapi index. Stashes ids, documents, and
        metadatas on the index instance for fast lookup at query time.
        Subsequent calls return the same instance. Process restart rebuilds.

    Returns:
        BM25Okapi or None: The BM25 index, or None if the vector store is
            empty (caller should fall back to dense-only retrieval).
    """
    global _bm25
    if _bm25 is None:
        from rank_bm25 import BM25Okapi
        if chroma_client.is_empty():
            return None
        result = chroma_client.get_all(include=["documents", "metadatas"])
        corpus = [tokenizer(doc) for doc in result["documents"]]
        bm25 = BM25Okapi(corpus)
        # Stash ancillary data on the instance for query-time lookup
        bm25._ids = result["ids"]
        bm25._documents = result["documents"]
        bm25._metadatas = result["metadatas"]
        _bm25 = bm25
    return _bm25


# ##############################################################################
# Cross-encoder reranker
# ##############################################################################


def _get_cross_encoder():
    """Lazy-load the cross-encoder model on first call.

    Approach:
        Constructs a sentence-transformers CrossEncoder using the model
        configured in CROSS_ENCODER_MODEL. The model downloads to the
        HuggingFace cache on first use (~80 MB for the default MS-MARCO
        MiniLM model). Subsequent process restarts read from cache.

    Returns:
        CrossEncoder: The reranker instance.
    """
    global _cross_encoder
    if _cross_encoder is None:
        from sentence_transformers import CrossEncoder
        _cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)
    return _cross_encoder


# ##############################################################################
# Hybrid retrieval primitive
# ##############################################################################


def retrieve(query: str, k: int = TOP_K, tokenizer=_default_tokenizer) -> list[Document]:
    """Return top-k LangChain Documents via hybrid retrieval + cross-encoder rerank.

    Args:
        query (str): The search query.
        k (int): How many top results to return. Defaults to TOP_K from config.
        tokenizer: BM25 tokenizer to apply to both the corpus (at index-build
            time) and the query. Must be the same callable for both, or
            tokens won't align. Defaults to lowercase + whitespace split.
            Pass alternates for ablation; clear `_bm25` first if changing
            tokenizer mid-process.

    Approach:
        Three-stage retrieval pipeline:

          1. **Hybrid retrieval**: dense (SPECTER2 cosine) and BM25 each
             produce a top-_FUSION_TOP candidate list. RRF fuses them into
             a single ranked list, taking the top-RERANK_TOP candidates.

          2. **Cross-encoder reranking**: for each candidate, the cross-encoder
             reads the (query, chunk) pair with cross-attention and produces
             a relevance score. The cross-encoder catches fine-grained
             relevance signals that bi-encoder retrievers smear away:
             specific number-row intersections in tables, formula content,
             phrase-level matches inside the right paper.

          3. **Final top-k**: chunks sorted by cross-encoder score; top-k
             returned.

        This is the single source of truth for production retrieval. The
        agent tool and the eval script both call this function so they
        always test the same thing.

    Returns:
        list[Document]: Top-k Documents in reranked score order. Empty list
            if the knowledge base is empty.
    """
    if chroma_client.is_empty():
        return []

    store = get_vector_store()

    # Dense retrieval: pull a wider net than k for fusion headroom
    dense_docs = store.similarity_search(query, k=_FUSION_TOP)
    dense_ranks = {d.id: rank for rank, d in enumerate(dense_docs, 1)}

    # BM25 retrieval: fall back to dense-only if BM25 isn't available
    bm25 = _get_bm25(tokenizer)
    if bm25 is None:
        return dense_docs[:k]
    query_tokens = tokenizer(query)
    scores = bm25.get_scores(query_tokens)
    bm25_top_idx = sorted(range(len(scores)), key=lambda i: -scores[i])[:_FUSION_TOP]
    bm25_ranks = {bm25._ids[i]: rank for rank, i in enumerate(bm25_top_idx, 1)}

    rrf_scores = _rrf_fuse(dense_ranks, bm25_ranks)

    # Take the top-RERANK_TOP for cross-encoder reranking (not top-k yet)
    rerank_pool_ids = sorted(rrf_scores, key=lambda c: -rrf_scores[c])[:RERANK_TOP]

    # Build Documents for each candidate (reuse dense where possible)
    dense_by_id = {d.id: d for d in dense_docs}
    candidate_docs: list[Document] = []
    for cid in rerank_pool_ids:
        if cid in dense_by_id:
            candidate_docs.append(dense_by_id[cid])
        else:
            idx = bm25._ids.index(cid)
            candidate_docs.append(Document(
                page_content=bm25._documents[idx],
                metadata=bm25._metadatas[idx] or {},
                id=cid,
            ))

    # Cross-encoder rerank: score each (query, chunk_text) pair
    ce = _get_cross_encoder()
    pairs = [(query, doc.page_content) for doc in candidate_docs]
    ce_scores = ce.predict(pairs)

    # Sort by cross-encoder score, take top-k
    ranked = sorted(zip(candidate_docs, ce_scores), key=lambda x: -x[1])
    return [doc for doc, _ in ranked[:k]]


# ##############################################################################
# Agent-facing wrapper
# ##############################################################################


def search_knowledge(query: str) -> str:
    """Search the research-paper knowledge base and format hits for the agent.

    Args:
        query (str): The user's search query.

    Approach:
        Delegates retrieval to retrieve() (which uses hybrid retrieval under
        the hood) and adds a presentation layer: arxiv_id, title, and
        section_heading in the header line so the agent can cite sources in
        its answer. Pure formatting; no retrieval logic lives here.

    Returns:
        str: Formatted results with citations, or a message indicating the
            knowledge base is empty or no relevant matches were found.
    """
    results = retrieve(query)
    if not results:
        return "No knowledge base found. Please ingest documents first."

    formatted = []
    for i, doc in enumerate(results, 1):
        meta = doc.metadata or {}
        arxiv_id = meta.get("arxiv_id", "unknown")
        title = meta.get("title", "Untitled")
        section = meta.get("section_heading", "")
        section_part = f" | {section}" if section else ""
        formatted.append(
            f"[{i}] arXiv:{arxiv_id} - {title}{section_part}\n"
            f"{doc.page_content}"
        )
    return "\n\n".join(formatted)


# ##############################################################################
# Source listing
# ##############################################################################


def list_sources() -> str:
    """List all documents currently in the knowledge base.

    Approach:
        Pulls every metadata record from the collection and counts chunks per
        arxiv_id. Returns a readable summary the agent can quote when asked
        "what's in the knowledge base".

    Returns:
        str: A summary line plus one row per document.
    """
    if chroma_client.is_empty():
        return "No documents ingested yet."

    metadatas = chroma_client.get_all()["metadatas"] or []

    counts: Counter = Counter()
    titles: dict[str, str] = {}
    for m in metadatas:
        arxiv_id = m.get("arxiv_id", "unknown")
        counts[arxiv_id] += 1
        if arxiv_id not in titles:
            titles[arxiv_id] = m.get("title", "")

    lines = [
        f"Knowledge base: {len(counts)} document(s), {sum(counts.values())} chunks total\n"
    ]
    for arxiv_id, count in counts.most_common():
        title = titles.get(arxiv_id, "")
        title_part = f" - {title}" if title else ""
        lines.append(f"  - arXiv:{arxiv_id}{title_part} ({count} chunks)")

    return "\n".join(lines)
