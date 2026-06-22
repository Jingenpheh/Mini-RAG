# ##############################################################################
# File: retriever.py
# Purpose: Retrieval surface for the agent. Queries the Chroma collection by
#          similarity and formats results for the LLM to read. Also lists what's
#          currently in the vector store.
#
# Contents:
#   Functions:
#     search_knowledge()       - Top-k similarity search, returns formatted hits
#     list_sources()           - Summary of documents and chunk counts in store
# ##############################################################################


# Standard library
from collections import Counter

# Local
from config import TOP_K
from tools.utils import get_vector_store


# ##############################################################################
# Search
# ##############################################################################


def search_knowledge(query: str) -> str:
    """Search the research-paper knowledge base for relevant chunks.

    Args:
        query (str): The user's search query.

    Approach:
        Embeds the query via the same model used at ingestion (configured in
        utils.get_embedder), runs a top-k cosine search against Chroma, and
        formats the hits with their source paper and section heading so the
        agent can cite them in the answer.

    Returns:
        str: Formatted results with citations, or a message indicating the
            knowledge base is empty or no relevant matches were found.
    """
    store = get_vector_store()

    # If vector store is empty, signal the agent to ingest documents first
    if store._collection.count() == 0:
        return "No knowledge base found. Please ingest documents first."

    # Top-k similarity search
    results = store.similarity_search(query, k=TOP_K)

    if not results:
        return "No relevant information found for your query."

    # Format each hit with paper-level and section-level context
    formatted = []
    for i, doc in enumerate(results, 1):
        meta = doc.metadata or {}
        arxiv_id = meta.get("arxiv_id", "unknown")
        title = meta.get("title", "Untitled")
        section = meta.get("section_heading", "")
        section_part = f" | {section}" if section else ""
        formatted.append(
            f"[{i}] arXiv:{arxiv_id} — {title}{section_part}\n"
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

    # Count chunks per arxiv_id, and remember the title for display
    counts: Counter = Counter()
    titles: dict[str, str] = {}
    for m in metadatas:
        arxiv_id = m.get("arxiv_id", "unknown")
        counts[arxiv_id] += 1
        if arxiv_id not in titles:
            titles[arxiv_id] = m.get("title", "")

    # Format as a readable summary
    lines = [
        f"Knowledge base: {len(counts)} document(s), {sum(counts.values())} chunks total\n"
    ]
    for arxiv_id, count in counts.most_common():
        title = titles.get(arxiv_id, "")
        title_part = f" — {title}" if title else ""
        lines.append(f"  - arXiv:{arxiv_id}{title_part} ({count} chunks)")

    return "\n".join(lines)
