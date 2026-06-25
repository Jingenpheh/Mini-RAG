# ##############################################################################
# File: retriever.py
# Purpose: Retrieval primitives and agent-facing wrappers. The retrieve()
#          function is the single retrieval surface that both the agent's
#          search_knowledge tool and the eval script call. Production retrieval
#          behavior lives here; everything else is a presentation layer on top.
#
# Contents:
#   Functions:
#     retrieve()               - Top-k similarity search, returns Documents
#     search_knowledge()       - Agent-facing wrapper; formats hits as text
#     list_sources()           - Summary of documents and chunk counts in store
# ##############################################################################


# Standard library
from collections import Counter

# Third-party
from langchain_core.documents import Document

# Local
from config import TOP_K
from tools.utils import get_vector_store


# ##############################################################################
# Retrieval primitive
# ##############################################################################


def retrieve(query: str, k: int = TOP_K) -> list[Document]:
    """Return top-k LangChain Documents for the given query.

    Args:
        query (str): The search query.
        k (int): How many top results to return. Defaults to TOP_K from config.

    Approach:
        Calls similarity_search on the shared Chroma vector store. The query
        is embedded via the shared embedder (SPECTER2 in current setup) and
        ranked against the indexed chunks. This is the single source of truth
        for production retrieval behavior; the agent tool and the eval script
        both go through this function so they always test the same thing.

    Returns:
        list[Document]: Top-k Documents in similarity order (best first). Empty
            list if the knowledge base is empty.
    """
    store = get_vector_store()
    if store._collection.count() == 0:
        return []
    return store.similarity_search(query, k=k)


# ##############################################################################
# Agent-facing wrapper
# ##############################################################################


def search_knowledge(query: str) -> str:
    """Search the research-paper knowledge base and format hits for the agent.

    Args:
        query (str): The user's search query.

    Approach:
        Delegates retrieval to retrieve() and adds presentation layer:
        arxiv_id, title, and section_heading in the header line so the agent
        can cite sources in its answer. Pure formatting; no retrieval logic
        lives here.

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
    store = get_vector_store()

    if store._collection.count() == 0:
        return "No documents ingested yet."

    metadatas = store._collection.get()["metadatas"] or []

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
