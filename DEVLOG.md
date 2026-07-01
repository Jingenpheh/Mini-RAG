# Mini-RAG Development Log

## 1. Project goal

Mini-RAG is a single-corpus RAG over arXiv ML/AI research papers, exposed as an MCP server so external agents can consume it as a memory tool. This doc walks the v1 to v5 design journey: ingestion pipeline, chunking strategy, hybrid retrieval, reranking, contextual chunking, eval-driven iteration, and the MCP wrap.

For "what does this repo do today" the README has the headline numbers and stack. This doc is the journey, not the architecture.

---

## 2. Summary and status

The system is at v6. The MCP wrapper is in place. On a 30-question golden eval set drawn from the corpus, retrieval-side numbers went from Recall@5 = 0.103 at the v1 baseline to Recall@5 = 0.690 at v6 (about 6.7x), MRR went 0.059 to 0.541 (9.2x). RAGAS LLM-judged metrics: faithfulness went 0.634 to 0.876, context recall 0.169 to 0.661, answer correctness 0.267 to 0.505. The README has the full headline table. The v5 to v6 step was an ablation-driven tokenizer change for BM25, not an architectural change.

**Metrics in brief** (so the numbers below carry meaning even if these terms are unfamiliar):

- **Recall@k**: did any gold-labelled chunk appear in the top-k retrieved? Deterministic, 0 to 1, higher is better.
- **MRR (Mean Reciprocal Rank)**: 1 over the rank of the first gold chunk in the result list, averaged across the set. Rewards getting the right chunk near the top.
- **NDCG@k**: position-weighted score that handles multi-gold questions. Rewards getting all gold chunks high in the ranking.
- **Faithfulness, context recall, answer correctness** (RAGAS, LLM-judged on a 0 to 1 scale, computed over a minimal generation step that takes the retrieved chunks and answers the question): faithfulness asks whether the generated answer is supported by the chunks (no hallucination), context recall asks whether the chunks contain the information needed to answer, answer correctness asks whether the generated answer matches the gold answer. Section 3.3 has the longer treatment.

**Current stack**:

- Parsing: Docling, called directly (not via `langchain-docling`)
- Chunking: paragraph-level via docling `doc_items`, with merge / drop / split refinements
- Embeddings: SPECTER2 (Allen AI, 768-dim, paper-specialized, runs locally)
- Vector store: Chroma (local SQLite)
- Retrieval: hybrid (BM25 + dense via Reciprocal Rank Fusion), then cross-encoder reranking (`ms-marco-MiniLM-L-6-v2`), then top-k. BM25 tokenizer is hyphen-aware split plus Porter stemming (snowballstemmer), adopted at v6 after ablation
- Eval: custom deterministic retrieval metrics (Recall@k, MRR, NDCG) plus RAGAS LLM-judged metrics
- Production interface: MCP server (`mini_rag/mcp_server.py`)

### Key design decisions

The seven calls that drove most of the improvement and most of the doc:

- **Paragraph-level chunking via Docling `doc_items` directly**, not `langchain-docling`'s `HierarchicalChunker` and not semantic chunking. Research papers are already paragraph-segmented by the author, so the document's own structure is the cheapest reliable signal. See section 3.1.
- **Hybrid retrieval (BM25 + dense via RRF) plus cross-encoder reranking.** Diagnosed from the v1 baseline's failure modes: specific_fact_lookup, methodology, equation, and table_numerical all came in near zero. Dense alone misses exact-term anchors (acronyms, named systems, numbers); BM25 fills that gap; reranking catches "right region, wrong specific chunk." See sections 4.4 and 4.5.
- **Contextual chunking prefix** (paper title and section heading prepended to every chunk before embedding and BM25 indexing). Fixes the class of failures where the chunk holding the answer doesn't contain the paper's distinctive name, so neither dense embedding nor BM25 has an in-text anchor to grip onto. See section 4.6 for the concrete example.
- **Tokenizer for BM25: hyphen-aware split plus Porter stemming** (adopted at v6 after an ablation against five other variants). Splitting hyphens lets a query naming "SARLO" match the chunk token "sarlo-80"; Porter stemming collapses morphological variants ("embeddings" matches "embedding", "trained" matches "training"). See section 4.8.
- **SPECTER2 over OpenAI `text-embedding-3-small`.** Domain-specialized for academic papers, runs locally, no per-token cost. See section 3.4.
- **Eval set built before the MCP wrap.** The golden set is the contract that defines what "the RAG" is supposed to do. Every change after the baseline was measured against it. See section 3.3.
- **Auto-populated pipeline versioning** (`pipeline_commit` git SHA plus `config_hash`) used as both metadata and dedup key. Bumping the chunker version invalidates dedup, so the next ingestion run treats the corpus as fresh and re-processes it under the new config. No manual "bump the version constant, remember to wipe the collection" discipline that rots. See section 3.1.
- **MCP for the production interface, dev agent kept only as a smoke test.** External agents consume retrieval through the MCP server; the LangChain `dev_agent.py` is for local sanity checks during development. See section 4.9.

### Per-version progression

"v1" in this table is the first arXiv-era measured baseline. The earlier AMD-blog predecessor (covered in section 4.1) ran only manual smoke tests on a five-document corpus and didn't produce formal Recall@k or RAGAS numbers, so it's not on this table.

| Version | Change | Recall@5 | RAGAS deltas |
|---|---|---|---|
| v1 | First measured baseline: Docling parse + paragraph chunking + SPECTER2 + dense retrieval only, on the 50-paper arXiv corpus | 0.103 | (baseline) |
| v1.1 | Formula chunker fix (Docling `FormulaItem.orig` fallback) | flat | context_recall +0.034 |
| v2 | Hybrid retrieval: BM25 + dense via RRF | 0.103 to 0.276 | most RAGAS metrics jump |
| v3 | Cross-encoder reranking (top-RERANK_TOP fused candidates) | 0.276 to 0.310 | faithfulness slightly up |
| v4 | Contextual chunking prefix on every chunk | 0.310 to 0.517 | contribution_recall and cross_paper hit 1.000 |
| v5 | Widened RERANK_TOP from 20 to 50 | flat at 0.517 | context_recall +0.133, faithfulness +0.037 |
| v6 | BM25 tokenizer: hyphen-aware split + Porter stemming (ablation-driven) | 0.517 to 0.690 | equation 0.500 to 1.000; table_numerical 0.000 to 0.333; no per-type regressions |

### Done

Ingestion pipeline (parse, QC, chunk, embed, store), hybrid retrieval, cross-encoder reranking, contextual chunking, 30-question golden eval set, RAGAS integration, MCP server with 4 tools and 5 resources, deployment verifier (`mini-rag-check`).

### Next phase (planned, not yet built)

**Librarian agent.** Add a `librarian` agent inside the RAG that handles autonomous corpus management (monitoring sources, ingesting new papers, pruning unused chunks, surfacing analytics) and provides opt-in query-side capabilities (query rewriting, decomposition, generation) through dedicated MCP tools. The fast-retrieval hot path stays unchanged: external agents that want raw chunks still hit `search_knowledge` directly. The librarian opens a second channel for direct users (or agents) that want the full RAG experience, including query understanding and generation. This pulls in the query-understanding / decomposition / generation capabilities that the current RAG-as-service framing left out, without compromising the service contract. Details in section 5.

### Queued (after librarian)

Table-aware reranking (v5 left `table_numerical` at 0.000), parent-document retrieval, document preprocessing routing agent for non-paper doc types, tracing (Langfuse or Phoenix), local LLM swap for generation.

### How to read this doc

Section 3 collects the technical reasoning behind ingestion, retrieval, eval, and deferred decisions. Section 4 walks v1 to v5 chronologically with the diagnostic chain between each version. Section 5 is the queued work, with the librarian agent as the next phase.

---

## 3. Design deep dives

### 3.1 Ingestion

Picking up from the transition to arXiv papers (section 4.2). Once the corpus changed, the original ingestion pipeline stopped fitting. PyPDFLoader works for prose; it breaks on the multi-column layout, tables, figures, and equations papers actually contain.

**Parser choice**. PyPDFLoader was right for blog corpora and wrong for research papers. The realistic alternatives were Docling (IBM, free, local) and LlamaParse (LlamaIndex, paid above a free tier, cloud API). On research papers both produce good output. I went with Docling because it runs locally (no API, no recurring cost) and "I ran it locally" reads stronger than "I paid an API" for a portfolio piece.

First attempt used `langchain-docling`, which wraps Docling and returns LangChain `Document`s as a near-drop-in for `PyPDFLoader`. A quick test made the next problem visible: `DoclingLoader` runs Docling's `HierarchicalChunker` by default, which groups `doc_items` by section under a size budget. The grouping is inconsistent. Sometimes it lumps title + author + affiliation into one front-matter chunk (good), sometimes it lumps multiple body paragraphs into one super-chunk (muddy). The grouping isn't documented as deterministic. The fix was to drop the wrapper and call `docling.document_converter.DocumentConverter` directly, then drive chunking myself. That gave me a stream of raw `doc_items` to chunk over and final control over how chunks get formed.

**Routing point**. Docling won't handle every document type a real corporate input might include (scanned forms, slides, handwritten notes). I'm not building routing yet because I only have one document type, and designing routing for documents I don't have is premature abstraction. Instead, all ingestion calls go through one function, `parse_document(path)`, which currently just calls Docling. When routing becomes real, only that function changes; everything calling it stays the same.

**Chunking strategy**. I evaluated five alternatives:

- **Semantic chunking**: an embedding model finds boundaries by detecting similarity drops between adjacent sentences. The theoretically clean answer. Costs one embedding per sentence to find the breaks, and the benefit assumes the document has no existing semantic structure to lean on. For research papers the author already imposed semantic boundaries through sections and paragraphs, so this is doing the work twice. Earns its complexity on unstructured text, not on papers.
- **Hierarchical chunking with parent-doc retrieval**: small leaf chunks for embedding precision, larger parent chunks returned to the LLM for context. Doubles storage and adds a lookup step on every retrieval. Without an eval set to prove the gain, the cost wasn't worth paying. The schema is forward-compatible so this can be added later.
- **LLM-as-chunker**: pass the document to an LLM and have it mark chunk boundaries. The copy-paste failure mode is real (LLMs paraphrase, drop content, mangle special characters), scales linearly with corpus size, and isn't justified without baseline numbers.
- **Docling's `HierarchicalChunker`** (already rejected above for being non-deterministic).
- **Paragraph-level via docling's `DocumentConverter` directly**: iterate the raw `doc_items` in document order, one chunk per `doc_item`. For body content, one `doc_item` is one paragraph; for special structures, one `doc_item` is one list_item, one formula, one table, or one caption. Chunking semantics that don't depend on a heuristic grouper.

I went with the last one. The justification is the same one that ruled out semantic chunking: research papers are already paragraph-segmented by the author. Trusting that structure is cheaper than re-imposing one. I can change later if the eval shows paragraph chunking misses specific failure modes.

Two refinements layered on top of "one chunk per `doc_item`":

- **Small-item merge**: consecutive same-section same-label items under `CHUNK_MERGE_FLOOR` (200 chars) get merged. This re-creates the good `HierarchicalChunker` behavior for front matter (title, author, affiliation coalesce) without re-grouping body paragraphs.
- **Drop floor + size ceiling**: chunks under `CHUNK_DROP_FLOOR` (30 chars) are dropped (page numbers, stray artifacts). Chunks over `CHUNK_SIZE_CEILING` (2000 chars) are split on sentence boundaries.

**Artifacts** (formulas, tables, figures):

- **Formulas**: on extraction success, attach the LaTeX to the **preceding** chunk. The text leading into an equation usually names it ("we define forward diffusion by the SDE:"), which is what a query like "what SDE does the paper use" matches against. The text after an equation typically defines variables, which works as its own chunk. On extraction failure (placeholder `formula-not-decoded` detected by string match), drop the formula. The preceding text still describes its purpose.
- **Tables**: exported via Docling's `export_to_markdown(doc)`. Markdown preserves row and column relationships as text. Default Docling table output flattens to noisy `key. = value` strings with the 2D structure lost.
- **Figures**: skipped at this stage. Captions arrive as their own `caption` `doc_items` and are included in the embedding pool. A query about figure content matches the caption; the cited paper and page let the human inspect the actual figure.

**Embedding model**: SPECTER2 (`allenai/specter2_base`, 768-dim) over OpenAI's `text-embedding-3-small`. Domain-specialized for academic papers, runs locally via sentence-transformers, no per-token cost. First use downloads ~400 MB to the Hugging Face cache. The portfolio reasoning beats the operational cost (one extra dependency, roughly 3 to 5 minutes to embed 50 papers on CPU). The A/B comparison against OpenAI I deferred until an eval set existed; without numbers the choice would be guessing.

**Vector store**: Chroma kept. The shortlist was Chroma, pgvector, Qdrant, Weaviate, Pinecone, LanceDB. At 50 papers and roughly 7,400 chunks, every candidate handles the load comfortably. Chroma is `pip install` with data in `./chroma_db/`; everything else needs more infrastructure. The trigger to revisit is corpus growth past low-thousands of papers, where Chroma's hybrid-search story becomes the weakest.

**Metadata schema** (four sources, assembled at different points):

- **Intrinsic** (free, from the sourcing manifest): arxiv_id, title, authors, abstract, categories, published.
- **Parse-time** (from the parser): page, section_heading, region_type.
- **Derived** (computed by the pipeline): chunk_id, parent_chunk_id, char_count, config_hash, pipeline_commit.
- **Manual / external** (config-driven): pipeline_commit, ingested_at.

Per-chunk LLM enrichment (chunk summaries, Anthropic-style contextual prefixes) I considered and skipped: cost scales with chunk count and the gain is uncertain without an eval set to measure. The lightweight version of contextual chunking went in at v4 (section 4.6), prepending title and section without LLM calls.

**Versioning and dedup**. A `pipeline_version = "v1.0"` constant that I bump manually is the kind of discipline that works for the first month and silently rots. I dropped manual versioning and use two auto-populated fields instead:

- `pipeline_commit`: the current git SHA, captured by running `git rev-parse --short HEAD` at ingestion start.
- `config_hash`: a SHA-256 of the JSON-serialized values of the ingestion-relevant config (embedding model, chunk size, parser choice, chunker version).

These two fields also form the dedup key. Before processing a document, the pipeline checks whether `arxiv_id + config_hash` is already in the vector store; if yes, the document is marked `skipped`. Consequence: bump `CHUNKER_VERSION` (or change any other ingestion-relevant config) and dedup automatically invalidates, forcing re-ingest under the new config. No "remember to wipe the collection" discipline required.

**Quality gates and the "loud failure" principle**. Most parsers don't fail loudly. They return text regardless of whether the text is meaningful, and that gibberish gets chunked, embedded, and lands in the vector DB where it pollutes future queries. Five cheap heuristics catch this in `parsing.quality_check()`:

1. **`too_short`**: extracted text under `INGEST_QC_MIN_CHARS` (default 200).
2. **`low_alnum_ratio`**: alphanumeric + whitespace ratio under threshold (likely garbled).
3. **`unexpected_language`**: `langdetect` reports a language different from expected.
4. **`no_paper_structure_markers`**: none of "abstract", "introduction", "conclusion", "references" appears in the text.
5. **`abstract_overlap_low`**: less than 30% of the manifest's known abstract vocabulary appears in the extracted text.

If any fail, the document moves into `debug/ingestion/problem_documents/` alongside a JSONL report listing the failure reasons. The PDF and its diagnosis sit side by side; no grep through a master log. The principle is loud failure preferred over silent pollution. Better to skip a document and surface it for review than to let bad content silently degrade retrieval quality.

### 3.2 Retrieval

The retrieval pipeline is three stages and lives in `mini_rag/retriever.py`:

1. **Hybrid retrieval**: dense (SPECTER2 cosine via Chroma) and BM25 (in-memory, built lazily from chunks in Chroma) each pull `_FUSION_TOP` (=20) candidates. Reciprocal Rank Fusion (`_RRF_K`=60) merges them into one ranked list, taking the top `RERANK_TOP` (=50) into the rerank pool.
2. **Cross-encoder rerank**: each (query, chunk) pair is scored by the cross-encoder model (`ms-marco-MiniLM-L-6-v2`). The cross-encoder catches fine-grained signals that bi-encoder retrieval smears out: number-row intersections in tables, formula content, phrase-level matches inside the right paper.
3. **Final top-k**: chunks sorted by cross-encoder score, top-k returned (default `TOP_K`=5).

This is the single source of truth for production retrieval. The dev agent's `search_knowledge` tool, the MCP server's `search_knowledge` tool, and the eval runner all call `retrieve()` so they always exercise the same logic.

The diagnostic chain that led to each stage (hybrid in v2, reranking in v3, contextual prefix in v4, wider pool in v5) is in sections 4.4 through 4.7. Reading those in order gives the "why each stage exists" story.

**What this retrieval still can't do** (and why that's a scope decision, not a failure):

- **Multi-hop questions** require finding A, formulating a follow-up query about A, then returning B. Single-pass retrieval has no decomposition step.
- **Cross-paper questions** that don't name both papers explicitly require synthesizing across distant documents. A single embedding cannot equally serve two unrelated topics. (The v4 contextual prefix accidentally solved the named case; the harder case remains.)
- **Vague-ambiguous questions** ("tell me about image editing") have no anchor for the system to grip onto.

These belong in the agent layer that consumes this RAG, per the section 4.3 scope decision. Their zero scores in the eval are evidence of where the boundary lies. The librarian agent (section 5) is the planned answer to all three.

### 3.3 Evaluation

**Why the eval was built before the MCP wrapper**: the eval set is the contract. These are the questions the system is supposed to answer well. Once that's stable, the MCP tool surface that exposes the RAG has a measurable definition behind it. Building MCP first and evaluating second would be backwards. The other reason: I learned more from running the v1 baseline than from any single architectural decision in this project. The baseline numbers told me exactly which categories worked and which failed, which directly drove the v1.1 chunker fix, the v2 hybrid retrieval upgrade, and everything after.

**Two layers of metrics**:

- **Custom deterministic**: Recall@1, Recall@3, Recall@5, MRR, NDCG@5. Computed from chunk_id matching against the golden set. No LLM cost, no API spend. Tells me whether the right chunk was retrieved.
- **RAGAS LLM-judged**: faithfulness, context_precision, context_recall, answer_correctness, answer_relevancy. LLM-judged on top of a minimal generation step. Tells me whether the retrieved chunks were usable beyond strict chunk_id match.

The two-layer split saved me from over-correcting at one point. The v1 baseline showed `methodology` Recall@5 = 0 but `context_precision` = 0.904. That gap meant the retriever was finding **relevant** content from the right paper, just not the specific chunk I had marked as gold. The chunk_id strict match was over-punishing; the LLM-judge metric saw through to "this is methodology content from the right paper." Without RAGAS I would have widened the `gold_chunk_ids` to soften the metric. With RAGAS I could leave them and let context_precision carry that signal.

The eval-time generation step that RAGAS needs an answer for is deliberately minimal: no agent loop, no tool use, just "given these chunks, answer this question." That's a floor on what any reasonable consumer of the RAG could produce.

**Question typology**: 30 questions across 11 categories. Each category tests a different property. Three categories (`cross_paper`, `multi_hop`, `vague_ambiguous`, 4 questions total) were deliberately included **knowing** they would score zero at the RAG layer. Their value is to document where the section 4.3 boundary lies.

**The question-crafting principle**: eval questions for a context-less retriever must carry their own disambiguation. The first draft of the golden set had questions like "What dataset did this paper use?" and "What evaluation metrics did the team use in this paper?". They made sense to me looking at a specific paper, where "this paper" was implicit context. The retriever has no implicit context. SPECTER2 maps "What dataset did this paper use" into a fuzzy cloud of dataset-related content across all 50 papers; "this paper" is meaningless to a system processing a standalone query. The retrieval scores came back near zero even though the answers were trivially in the corpus.

I rewrote 14 of the 30 questions with explicit anchors:

- "What dataset did this paper use?" became "What dataset is introduced by SARLO-80?"
- "What evaluation metrics did the team use?" became "What evaluation metrics does CalTennis use for monocular-to-3D tennis pose estimation?"
- "What is the third takeaway of the experiment in this paper?" became "In the Calibrated Mixture-of-Experts under Distribution Shift paper, what is the third takeaway from the experiments?"

The anchor doesn't have to be the full paper title. The most effective rewrites used the paper's distinctive proper noun: a system name (SARLO-80, CalTennis, MAA, ACE, JanusMesh), a method name, or a technical phrase that appears in the chunk content. arxiv_ids don't help because the ID isn't in the chunk text. The principle generalizes: any eval set for a stateless retriever has this trap, and the fix is to bake disambiguation into the question itself.

**Reproducibility**: the arxiv papers in `docs/` are gitignored (250 MB) and the original `fetch_papers.py` pulls by category and date, which is non-deterministic. A small lock file at `scripts/sourcing/eval_corpus.json` lists the exact 50 arxiv_ids the eval set is built against. `fetch_papers.py --eval-corpus` queries arxiv by id_list (deterministic, no date or category filter) and downloads those papers. A fresh clone can reproduce the eval environment with one command, the repo stays small, and the eval still has the realistic 50-paper distractor corpus that makes retrieval testing meaningful.

### 3.4 Deferred decisions worth flagging

- **Embedding-model A/B comparison (SPECTER2 vs OpenAI 3-small)**: deferred. Without an eval set there was no way to attach numbers to the choice. The trigger to revisit: if Recall@5 stalls after retrieval tuning is exhausted, embedding-model comparison becomes the next lever.
- **Vector DB swap**: deferred. Chroma handles the current corpus comfortably. The known weakness is hybrid-search at scale, so a corpus growing past low-thousands of papers would flip the calculation toward pgvector or Qdrant.
- **GPU acceleration**: considered, deferred. SPECTER2 embedding on CPU takes 15-20 min on the 7,400-chunk corpus and would drop to 1-2 min on a consumer NVIDIA GPU. The runtime side is one line (read `os.environ.get("DEVICE")`, pass to `SentenceTransformer`). The install side is where it falls apart: PyTorch's CUDA wheels live on `download.pytorch.org/whl/cu124` (or `cu121`, `cu118`), the wheel has to match the user's CUDA driver, and there's no clean way to do this in `pyproject.toml`. The two paths are (1) a uv dependency group plus `[tool.uv.sources]` pinning torch to the right pytorch.org index, requiring users to know their CUDA version, or (2) a custom install script that runs `nvidia-smi`, parses the driver version, and pip-installs the right wheel. The install-script approach reads wrong for a portfolio repo (conventional for end-user apps like ComfyUI, not for libraries) and the long tail of edge cases (nvidia-smi not on PATH on Windows, WSL2 reporting differently, multi-GPU, AMD ROCm, Apple MPS, torch installed but DLL load error) means the user who actually has a problem still debugs manually. GPU stays out of the default install path. Anyone with a GPU pays the standard ML-ecosystem cost: install CUDA-enabled torch themselves the way they already know how.
- **LangGraph vs `create_tool_calling_agent`**: ReAct loop kept. Revisit when the agent loop pushes back on implicit state.
- **BM25 index persistence**: deferred. The BM25 index currently rebuilds from chunks in Chroma on every process start, about 1 second at 7,500 chunks. Persisting via pickle plus an invalidation hash (chunk count + sorted chunk_ids) is around 50 lines of code, but a 1-second cold start is invisible at this scale and the cache adds a stale-index risk that the rebuild-every-start approach doesn't have. Trigger to revisit: corpus past roughly 30k chunks (where the rebuild scales toward 5 seconds and starts being noticeable on the first query after process start) or the MCP server seeing frequent restarts in deployment. An alternative path is adopting Chroma's native hybrid search (newer versions support it), which would delete the hand-rolled BM25 code entirely but requires a Chroma version upgrade and might shift the eval numbers the v2 to v5 narrative depends on.

---

## 4. The v1 to v5 journey

### 4.1 v1: AMD-blog baseline

The first version was tutorial-grade by design. The corpus was five short AMD blog posts. The pipeline used PyPDFLoader for parsing, `RecursiveCharacterTextSplitter` at 500 characters with 100 overlap for chunking, OpenAI's `text-embedding-3-small` for embeddings, GPT-4o-mini for the LLM, ChromaDB for the vector store, and a LangChain `create_tool_calling_agent` ReAct loop with three tools (`search_knowledge`, `ingest_documents`, `list_sources`). No eval set; testing was three documents, fifty chunks, and manual spot checks.

Decisions worth flagging from this phase:

- **ReAct over Plan-and-Execute, Reflection, or multi-agent.** Knowledge retrieval is a short-horizon task: search, look at the results, decide, answer. Long-range planning isn't required, and the ReAct loop via `create_tool_calling_agent` handles "search, evaluate, retry" naturally.
- **LangChain over LlamaIndex.** This project is agent-first (retrieval is one tool among several), so LangChain's flexible orchestration was a better fit than LlamaIndex's more opinionated RAG pipeline.
- **Corrective RAG via prompt engineering, not a separate eval step.** I considered adding an LLM-judged evaluation chain between retrieval and generation. The agent already handles this through ReAct ("rephrase the query if results don't answer, max 2 retries, then check for new documents to ingest"). The prompt-engineered version is a simpler system with no extra LLM calls; the tradeoff is less explicit control, fine at this scope.

The system prompt went through three iterations during this phase: too-loose ("don't hallucinate" silently fell back to training data on out-of-corpus questions), too-strict ("NEVER generate information not returned by your tools" refused casual conversation), and finally a balanced version where the agent can use general knowledge but must label unsourced answers explicitly.

**What broke on the AMD corpus that motivated the rewrite**:

- PDFs saved from Chrome were image-only. PyPDFLoader returned zero characters because there was no text layer.
- Even text-layer PDFs came back with one word per line and excessive whitespace. A `re.sub(r"\s+", " ", text)` cleanup worked but the underlying parser couldn't be trusted.
- Web-page PDFs included LinkedIn share buttons, cookie banners, and navigation chrome embedded as text. All of it got chunked and embedded alongside content.

The takeaway: a fixed parsing pipeline breaks the moment it sees a document it wasn't built for. Different documents need different strategies. That insight became the routing-point reservation in section 3.1.

---

### 4.2 Transition: AMD blogs to arXiv papers

Five short blog posts wouldn't surface real RAG problems. Most of what makes RAG hard (layout, tables, equations, multi-column text, figure references) was absent from the AMD corpus. I needed a harder corpus.

arXiv research papers were the obvious choice. The pick felt simple and hard at the same time:

- **Simple**: arXiv has a public API and direct PDF URLs. No auth, no scraping, no rate-limit pain at moderate use. A fetcher script that pulls by category and date and deduplicates against a local manifest covers the whole pipeline.
- **Hard**: research papers run 8 to 30 pages, layout is two-column, tables are dense, equations are referenced inline, figures carry information that flat token extraction loses. Exactly the corpus that forces engagement with parsing and chunking instead of skipping them.

I built the fetcher at `scripts/sourcing/fetch_papers.py`. Default config pulls from `cs.AI`, `cs.LG`, `cs.CL`, `cs.CV`, `cs.IR`, `stat.ML`, with deduplication by canonical arXiv ID against a manifest at `scripts/sourcing/manifest.json`. The first run brought down 50 papers.

The folder convention I settled on was: `docs/` is data the RAG reads, `scripts/` is utilities the developer runs outside the RAG runtime, `tools/` (later renamed `mini_rag/`) is what the runtime calls. The sourcing dependency (`arxiv`) lives in a uv dependency group so the main runtime stays lean.

The ingestion pipeline got rebuilt from scratch against the new corpus shape: Docling for parsing, paragraph-level chunking, SPECTER2 for embeddings. The full design reasoning behind each choice is in section 3.1.

---

### 4.3 Scope: RAG-as-service, not an agent (initial framing)

Before going deep on retrieval, I had to answer a different question: what kind of RAG system am I actually building? Two paths were in front of me:

- **Agentic RAG**: the RAG itself owns an agent that decomposes queries, calls retrieval multiple times, self-corrects across passes, and produces a final answer.
- **RAG-as-service**: the RAG only handles ingestion and retrieval. It returns chunks. An external agent does the query understanding, decomposition, synthesis, and generation.

I went with RAG-as-service for the v1 to v5 cycle. The reasoning:

- The longer-term plan is for this RAG to be consumed by an upstream agentic pipeline that already does query understanding and orchestration. Putting an agent inside the RAG and exposing it to an outer agent means two agents fighting over the same state, with the inner one potentially modifying or paraphrasing content the outer one wanted raw. MCP fits the service framing naturally.
- Keeping scope tight meant I could actually deliver measurable quality on ingestion and retrieval. Trying to build query rewriting, decomposition, and generation in parallel on a single-corpus academic-paper RAG would have spread the eval-driven iteration thin.
- The scope decision shows up in the eval: the golden set deliberately includes `cross_paper`, `multi_hop`, and `vague_ambiguous` categories that I expected to score zero. Their zero scores aren't retrieval failures, they're consequences of the service boundary. They live in the agent layer that consumes this RAG.

The next phase walks part of this scope back. The librarian agent (section 5) brings query understanding, decomposition, and generation in as opt-in capabilities behind separate MCP tools, without compromising the fast-retrieval hot path. The v1 to v5 work below was all done within the initial service-only framing.

---

### 4.4 v2: hybrid retrieval (BM25 + dense via RRF)

Before talking about the retrieval upgrade, one chunker bug from the v1 baseline run worth noting. Docling's `FormulaItem` was returning empty `text` for failed formula extractions and my chunker was dropping those items entirely; papers with equations were losing the equation chunks. Fix: fall back to `FormulaItem.orig` (the raw source string) when `text` is empty. Tagged this as v1.1 in the eval results. Effect on retrieval rank was nil (Recall@5 stayed at 0.103), but it put formula content back in chunks so v2 had something to find. Necessary scaffolding, not a real improvement on its own.

The v1 baseline eval gave me the diagnostic I needed. Per-type breakdown: `definition` and `contribution_recall` worked. `specific_fact_lookup`, `methodology`, `equation`, and `table_numerical` all came in near zero.

The failure pattern was consistent. SPECTER2 was trained for paper-to-paper similarity. Asked something like "What dataset is introduced by SARLO-80?", it mapped the query into a fuzzy cloud of dataset-related content across all 50 papers. The chunk that actually answered the question contained the specific terms ("Umbra Collection", "SICD scenes", "2,565") but didn't repeat the paper's own name. Dense alone couldn't bridge from the question's anchor to the answer chunk's content terms.

Two paths to try:

- **Sentence-level chunking**: smaller chunks means tighter semantic match between question and chunk. Adds complexity and the gain on this specific failure mode wasn't guaranteed.
- **BM25 hybrid**: run a keyword retriever in parallel with the dense one and fuse the rankings. BM25 catches what dense misses (exact-term matching on acronyms, numbers, proper nouns) and dense catches what BM25 misses (semantic paraphrase, conceptual matching). Each fills the other's gap.

I went with hybrid first because it was the smaller change and the failure mode pointed directly at it.

**Fusion via Reciprocal Rank Fusion (RRF), not weighted score combination.** Each retriever produces a ranked list; RRF scores each chunk as `sum of 1/(K + rank)` across both lists with K=60. The rank-based fusion is robust across very different scoring scales, which weighted score combinations aren't.

**Numbers**: Recall@5 went from 0.103 to 0.276 (2.7x). The `equation` type went from 0.000 to 0.500 (combined with the v1.1 chunker fix). Categories that needed the agent layer (`cross_paper`, `multi_hop`, `vague_ambiguous`) stayed at zero, as expected from the scope decision in section 4.3.

---

### 4.5 v3: cross-encoder reranking

The v2 audit showed two distinct failure modes remained:

1. The gold chunk was in the fused top-20 but ranked between 6 and 20. Reranking can fix this.
2. The gold chunk was past rank 100 in both BM25 and dense (Q01 SARLO-80 at rank 200+, Q07 MAA at rank 1868). No reranker can recover what was never retrieved in the candidate pool.

I added a cross-encoder reranking stage to fix category 1. The flow became: dense top-20 plus BM25 top-20 fused by RRF, then the top-`RERANK_TOP` of the fused pool rescored by a cross-encoder, then top-k returned. The cross-encoder reads (query, chunk) pairs with cross-attention, scoring relevance directly rather than via independent embeddings.

**Model**: `cross-encoder/ms-marco-MiniLM-L-6-v2` from sentence-transformers. 80 MB, MS-MARCO trained, runs on CPU in under a second for a pool of 50. The standard small cross-encoder, chosen for the CPU constraint and because MS-MARCO is the right training domain (text passage relevance).

**Numbers**: Recall@5 went from 0.276 to 0.310. The reranker held context_recall flat and lifted faithfulness slightly. The deep failures (Q01, Q07) stayed at zero because the chunks weren't in the candidate pool. That confirmed the v2 audit diagnosis: the next fix had to be at the candidate-generation layer, not the rescoring layer.

---

### 4.6 v4: contextual chunking

The v3 audit confirmed the rank-200+ failures came from a structural mismatch. Q01 asked about SARLO-80, a system named in the paper. The chunk holding the answer didn't say "SARLO-80" anywhere; the paper introduced the name once on page 1 and used "our system" thereafter. SPECTER2 embedded the chunk as generic methods text. BM25 had no token to match. Both retrievers missed.

The fix was simple: prepend a contextual prefix to every chunk before embedding and BM25 indexing.

```
Paper: <title>
Section: <section heading>

<original chunk text>
```

Every chunk now carried the paper's title and the section heading inside its searchable text. The chunk's metadata kept `title` and `section_heading` as separate fields for filtering and citation rendering, but the searchable text was what the retrievers scored against.

**Why inline prefix and not a separate weighted metadata field**:

- Both BM25 and dense benefit from one prefix string without any retriever-side changes.
- The cross-encoder also sees the prefix at rerank time, so the title context flows into the rescoring decision.
- It's reversible at display time by stripping the known prefix format.

**Numbers**: Recall@5 went from 0.310 to 0.517. The per-type lifts landed where I expected and one place I didn't:

- `contribution_recall`: 0.333 to 1.000. "What are the contributions of <paper>" now matches because the title is in every chunk.
- `methodology`: 0.000 to 0.500. Section-heading prefix helps "how did they do X" find the methods section.
- `cross_paper`: 0.000 to 1.000. **Surprise**. I had predicted this category would need the agent layer (per section 4.3) but the embedding gain from per-chunk paper disambiguation was enough for the two specific cross-paper questions in the eval. The chunks now disambiguate which paper they came from at the embedding layer, so cross-paper queries that name both papers retrieve from both.
- `table_numerical`: 0.000 to 0.000. The cross-encoder still doesn't rerank table-format chunks well (model fit, not pool depth).
- `multi_hop` and `vague_ambiguous`: 0.000. Still agent-layer problems, as predicted.

I bumped `CHUNKER_VERSION` from 2 to 3. The change invalidates `config_hash`, which forces the ingest pipeline to re-process the whole corpus under the new chunking. Without the bump, the dedup check (section 3.1) would have skipped re-ingest and v4 would have run against v3 chunks.

---

### 4.7 v5: widened RERANK_TOP to 50

v4 fixed the deep failures by getting the right chunks into the candidate pool. The next question: does a wider rerank pool help? The cross-encoder was rescoring the top-20 of the fused result. If gold chunks were landing at ranks 21 through 50 in the fused output, widening the pool would catch them.

I widened `RERANK_TOP` from 20 to 50 and re-ran. Strict Recall@5 stayed at 0.517. Per-question diffs were small and went both ways.

But the LLM-judged metrics moved:

- `context_recall`: +0.133
- `faithfulness`: +0.037

This is the latent-quality signal the strict chunk_id match doesn't reward. The strict metric only rewards "the exact gold chunk was returned." The LLM-judged metrics reward "the returned chunks let the model produce a faithful answer." Widening the rerank pool was pulling in adjacent chunks containing the answer content without matching the gold chunk_id. The minimal generator answered more questions correctly with the wider pool's top-5.

I kept `RERANK_TOP=50`. The cost is one cross-encoder pass on 50 instead of 20 candidates (about 25 ms more per query on CPU). The benefit is measurable on the metrics that actually reflect downstream answer quality.

---

### 4.8 v6: BM25 tokenizer ablation (porter+hyphen)

After a code review flagged the BM25 tokenizer as a place I'd never measured, I ran an ablation on the eval set. The script lives at `tests/ablation/bm25_tokenization.py`. It runs the full retrieval pipeline (hybrid + cross-encoder rerank) against the 30-question golden set under six tokenizer variants and reports Recall@k, MRR, NDCG@5 per variant, plus a per-question-type breakdown.

The six variants:

- `baseline`: `text.lower().split()` (the v5 tokenizer)
- `porter`: baseline + Porter stemming (collapses "embedding"/"embeddings", "trained"/"training" to the same token)
- `nostop`: baseline + English stopword removal
- `hyphen`: split on any non-word character (so "SARLO-80" becomes ["sarlo", "80"])
- `porter+nostop` and `porter+hyphen`: the combinations

The aggregate results:

| Variant | Recall@1 | Recall@3 | Recall@5 | MRR | NDCG@5 |
|---|---|---|---|---|---|
| baseline | 0.310 | 0.379 | 0.517 | 0.378 | 0.368 |
| porter | 0.379 | 0.448 | 0.586 | 0.447 | 0.447 |
| nostop | 0.276 | 0.414 | 0.517 | 0.363 | 0.356 |
| hyphen | 0.414 | 0.517 | 0.621 | 0.491 | 0.474 |
| porter+nostop | 0.310 | 0.483 | 0.552 | 0.401 | 0.408 |
| **porter+hyphen** | **0.448** | **0.586** | **0.690** | **0.543** | **0.514** |

Three things to note:

- **`porter+hyphen` lifted Recall@5 from 0.517 to 0.690.** That's a +0.173 absolute gain, on the same order as the v4 contextual chunking jump. MRR moved by +0.165.
- **`nostop` made things slightly worse.** Stopword removal dropped Recall@1 from 0.310 to 0.276. BM25's IDF already de-weights very common terms, so stripping them explicitly was removing signal. Documented as a negative result and not adopted.
- **No type-level regressions under `porter+hyphen`.** The per-type breakdown shows every question type either stayed the same or improved. Specifically: `equation` went from 0.500 to 1.000 (both equation questions now retrieved), and `table_numerical` finally moved off zero for the first time in the project (0.000 to 0.333). `multi_hop` and `vague_ambiguous` stayed at zero as predicted, since they remain agent-layer problems.

**Why the hyphen split mattered**: the v4 contextual chunking work made sure every chunk contained the paper's distinctive name (the SARLO-80 case in section 4.6). The v5 tokenizer was then partially undermining that fix because "SARLO-80" stayed as a single token that queries naming "SARLO" couldn't match. Splitting on non-word characters made v4's contextual prefix fully payable into BM25 ranking. End-to-end, the two changes compose.

**Why Porter and not a more sophisticated stemmer or lemmatiser**: stemming is rule-based truncation; lemmatisation is dictionary-based normalisation. For retrieval token-matching, BM25 doesn't need the output to be real words, only consistent. Porter is the standard small choice (snowballstemmer, ~1 MB, no corpora download). Lemmatisation would add weight (NLTK WordNet, or spaCy with a 50 MB English model) for an uncertain incremental gain. I'd file a lemmatisation ablation as a future direction rather than building it now.

The change in code: `mini_rag/retriever._default_tokenizer` is now `[porter.stemWord(t) for t in re.findall(r"\w+", text.lower())]`. Both the corpus indexing path and the query tokenization path use the same function (they must, or tokens don't align). `snowballstemmer>=2.2.0` is a main runtime dependency from v6 onward.

The ablation results (summary + per-type + per-question) are kept at `tests/ablation/bm25_tokenization_results.json` for reproducibility.

**RAGAS metrics after adoption**: after the tokenizer swap I re-ran the main eval (`tests/eval/run_eval.py`) against the full 30-question set so the LLM-judged layer had numbers too. Retrieval-side matches the ablation exactly (Recall@5 = 0.690, MRR = 0.541), which confirms the production default is what the ablation measured. RAGAS deltas from v5 (from the clean-commit re-run):

- **Faithfulness**: 0.826 to 0.876 (+0.050). The generated answer is better grounded in the retrieved chunks.
- **Context recall**: 0.608 to 0.661 (+0.053). Chunks now cover more of the gold answer material.
- **Context precision** (not tracked in v5 headline): 0.749 at v6.
- **Answer relevancy** (not tracked in v5 headline): 0.672 at v6.
- **Answer correctness**: 0.474 to 0.505 (+0.031). Every RAGAS metric now moves in the retrieval-consistent direction.

**A note on LLM-judge variance**: the first v6 eval (2026-06-30) actually recorded `answer_correctness` at 0.458, which was a small -0.016 dip vs v5. I flagged it at the time, hedging that it was probably LLM-judge noise. That first run was against an uncommitted working tree, which is a reproducibility gap the review round-2 called out. Re-running on 2026-07-01 against clean HEAD f9b3d0f produced 0.505 (+0.031 vs v5), confirming the earlier "dip" was variance. Retrieval numbers were byte-identical between runs (dense + BM25 + rerank is deterministic); RAGAS moved by a few percentage points because the LLM judge is stochastic.

Takeaway that stays in the writeup: LLM-judged scores at n=30 have real run-to-run variance. Anything under about ±0.03 shouldn't be treated as signal without a re-run or larger sample.

---

### 4.9 Structural cleanup and MCP wrap

Through v1 to v5, the repo accumulated leftovers from the AMD-demo origin. Before wrapping with MCP I cleaned the structure so the library boundary was clear.

- **`tools/` renamed to `mini_rag/`.** Generic name to project name. Used `git mv` to preserve history, then mass-updated nine files' imports.
- **Dev agent moved out of the library.** `agent.py` and `main.py` were at the project root, wiring the LangChain ReAct agent for local interactive testing. That's developer tooling, not library code. Consolidated into `scripts/dev_agent.py`. The dev agent stays in the repo because the LangChain interface is itself worth showing alongside the MCP one, but it's clearly a developer utility now.
- **Config consolidated.** `scripts/sourcing/config.py` and the root `config.py` were merged into one root file, with sourcing constants taking a `SOURCING_*` prefix. Every config value now supports an environment-variable override, which matters for MCP deployment: the consumer sets `INGEST_CORPUS_DIR` or `RERANK_TOP` in their MCP client config without forking the repo.
- **Smoke tests deleted.** `tests/test_ingest.py` and `tests/test_retriever.py` were initial smoke tests written before the eval framework existed. The eval runner at `tests/eval/run_eval.py` now exercises the full ingest-to-retrieve path across 30 questions with both deterministic and LLM-judged metrics. The smoke tests were exercising the same paths with less coverage. I deleted them. The instinct to keep "extra tests just in case" is wrong here: tests have a maintenance cost and the eval framework already covers what they covered.

Then the MCP wrap. The retrieval pipeline was stable and the eval numbers were documented, so the tool surface had a measurable definition behind it.

The MCP server exposes four tools and five read-only resources:

- **Tools** (actions, with arguments): `search_knowledge(query, k)`, `list_corpus()`, `ingest_new_documents()`, `ingest_from_arxiv(arxiv_id)`.
- **Resources** (read-only data, zero arguments): `eval://golden_set`, `eval://latest_results`, `eval://baseline_analysis`, `eval://v4_per_question_diagnosis`, `corpus://manifest`.

I considered exposing the eval data as tools instead. Two reasons I kept them as resources: they don't take arguments, and they don't change state. MCP resources are the right primitive for "here's a chunk of data clients can read." Tools are the right primitive for "here's a thing clients call." Mixing them muddles the contract.

I also considered a `configure(...)` tool that lets the consumer change retrieval parameters at runtime, and dropped it. Runtime configuration is a stateful concern, the values are deployment knobs rather than per-query knobs, and it makes eval runs harder to reproduce. The env-var override pattern from the config consolidation handles deploy-time tuning without needing a runtime tool.

Finally, `mini_rag/check_setup.py` is a separate utility: a small checklist (API key, corpus dir, Chroma reachable, MCP server importable, vector store collection populated) that reports green or red per item. It's the answer to "I cloned this and something doesn't work."

---

## 5. Future improvements

### Next phase: librarian agent

The RAG-as-service framing in section 4.3 left query understanding, decomposition, and generation outside the scope of v1 to v5. The next phase brings them back in through a **librarian agent** that lives inside the RAG and opens a second access channel without compromising the fast-retrieval hot path.

The librarian metaphor maps to RAG functions cleanly:

| Librarian function | RAG analogue |
|---|---|
| **Acquisition** (deciding what to add to the collection) | Autonomous ingestion: monitor target arxiv categories, fetch new papers on a schedule, run them through the standard ingest pipeline |
| **Cataloging** (classifying, tagging, organizing) | Metadata enrichment: doc-level summaries, derived fields, parent-chunk wiring |
| **Reference / readers' advisory** (helping patrons phrase what they need) | Query refinement and rewriting: when a user query is vague, the librarian rephrases or decomposes before sending to retrieval |
| **Collection development** (pruning outdated items, identifying gaps) | Prune chunks never retrieved; identify topic gaps in the corpus; recommend new sources |
| **Circulation** (tracking what's checked out) | Retrieval analytics: which chunks get returned often, which are dead weight |
| **Preservation** (keeping items intact) | Integrity checks: verify chunks haven't degraded, re-ingest if config_hash changed |
| **Recommendations** (related-titles service) | Cross-paper recommendations driven by the existing embedding store |

Two access channels:

- **Direct user channel through the librarian** (the full RAG experience): query understanding, decomposition, retrieval, generation, conversational follow-ups.
- **MCP retrieval channel** (unchanged): external agents that already do their own orchestration hit `search_knowledge` directly, fast, no agent in the loop.

The eval set has the placeholders for the next phase already in place. The `cross_paper`, `multi_hop`, and `vague_ambiguous` categories that scored zero through v5 (because they need an agent layer) become live tests once the librarian's query-decomposition is wired in. The eval will be re-run through the librarian to measure the lift.

### Queued behind the librarian

- **Table-aware chunking and reranking**. v5 left `table_numerical` at 0.000. The MS-MARCO MiniLM cross-encoder doesn't score table-row chunks well, and the current chunker splits tables into per-row pieces via Docling's structured output. Two threads: keep each table as one chunk (caption plus rows joined, conflicts with the size ceiling so needs a separate code path), or swap in a reranker trained on tabular content.
- **Parent-document retrieval**. Index small chunks for embedding precision, return larger parent sections to the LLM for context. Should lift `context_recall` further. The chunk schema is already forward-compatible.
- **Document preprocessing routing agent**. An agent that inspects each incoming document and routes it to the right parser (Docling for digital PDFs, OCR for scanned, structured table parser, slide parser). Replaces the fixed `parse_document` with adaptive routing.
- **Semantic chunking as a fallback option**. Currently deferred because docling's structural chunks were good enough. Worth revisiting if the eval surfaces specific failure modes that paragraph-level chunking can't address.
- **Tracing and cost tracking**. Wire Langfuse or Phoenix for per-request tracing during retrieval and the eval-time generation step. Useful both for debugging and for quantifying per-query cost as the system scales.
- **Local LLM swappable for generation**. Add a switchable backend so the eval-time generation step (and potentially the RAGAS judge calls) can run against a local model. Useful for privacy-aware use cases and lowers eval cost during iteration.
