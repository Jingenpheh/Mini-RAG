from collections import Counter
from config import TOP_K
from tools.utils import get_vector_store


def search_knowledge(query: str) -> str:
    """Search the AMD knowledge base for relevant information.

    Args:
        query: The search query to find relevant documents.

    Returns:
        Formatted string of relevant chunks with sources, or an error message.
    """
    store = get_vector_store()

    # If vector store is empty, signal the agent to ingest documents first
    if store._collection.count() == 0:
        return "No knowledge base found. Please ingest documents first."

    # Run similarity search — Chroma embeds the query and finds the closest chunks
    results = store.similarity_search(query, k=TOP_K)

    if not results:
        return "No relevant information found for your query."

    # Format results with source citations for the agent to read
    formatted = []
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "?")
        formatted.append(
            f"[{i}] Source: {source} (page {page})\n{doc.page_content}"
        )

    return "\n\n".join(formatted)


def list_sources() -> str:
    """List all documents currently in the knowledge base.

    Returns:
        Summary of ingested documents and chunk counts.
    """
    store = get_vector_store()

    if store._collection.count() == 0:
        return "No documents ingested yet."

    # Get all chunk metadata and count how many chunks each source document has
    metadatas = store._collection.get()["metadatas"]
    source_counts = Counter(m["source"] for m in metadatas)

    # Format as a readable summary for the agent
    lines = [f"Knowledge base: {len(source_counts)} document(s), {len(metadatas)} chunks total\n"]
    for source, count in source_counts.items():
        lines.append(f"  - {source} ({count} chunks)")

    return "\n".join(lines)
