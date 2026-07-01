# ##############################################################################
# File: chroma_client.py
# Purpose: Wrap all direct access to the underlying Chroma collection in one
#          place. The LangChain `langchain_chroma.Chroma` wrapper exposes the
#          underlying `chromadb.Collection` only as a private attribute
#          (`_collection`), and the pipeline needs raw access to it for two
#          reasons:
#            1. Bypass the wrapper's automatic re-embedding on write, since
#               the ingest pipeline computes SPECTER2 embeddings itself.
#            2. Read raw documents and metadatas (for the BM25 index, the
#               dedup check, and the corpus listing) without the wrapper's
#               Document-object packaging.
#
#          Touching a private attribute is brittle: LangChain reserves the
#          right to rename `_collection` in any minor release. Isolating that
#          access in one module means a future rename costs one edit here
#          rather than scattered edits across the codebase.
#
# Contents:
#   Functions:
#     count()                  - Number of chunks in the collection
#     is_empty()               - True if the collection has no chunks
#     get_all(include)         - Fetch all records (optionally with fields)
#     get_where(where, limit)  - Fetch records matching a where filter
#     add(...)                 - Insert chunks with pre-computed embeddings
# ##############################################################################


# Local
from mini_rag.utils import get_vector_store


# ##############################################################################
# Centralized private-attribute access
# ##############################################################################


def _collection():
    """Return the underlying chromadb.Collection.

    Approach:
        This is the single place in the codebase that touches the private
        `_collection` attribute of the LangChain `Chroma` wrapper. All other
        modules call into the helper functions below, which call this. If
        LangChain ever renames or refactors `_collection`, this is the one
        line to update.

    Returns:
        chromadb.Collection: The raw collection handle backing the wrapper.
    """
    return get_vector_store()._collection


# ##############################################################################
# Read helpers
# ##############################################################################


def count() -> int:
    """Return the number of chunks currently in the collection."""
    return _collection().count()


def is_empty() -> bool:
    """True if the collection has no chunks."""
    return count() == 0


def get_all(include: list[str] | None = None) -> dict:
    """Read every chunk from the collection.

    Args:
        include (list[str] | None): Fields to return per record
            (e.g. ["documents", "metadatas"]). When None, ChromaDB's default
            include set is used.

    Returns:
        dict: Keys include at least "ids"; "documents" and "metadatas" are
            present when requested via include or when in the ChromaDB
            default set.
    """
    if include is None:
        return _collection().get()
    return _collection().get(include=include)


def get_where(where: dict, limit: int | None = None) -> dict:
    """Read chunks matching a where filter.

    Args:
        where (dict): Chroma where-filter (e.g. {"$and": [{"arxiv_id": "X"},
            {"config_hash": "Y"}]}).
        limit (int | None): Max number of results to return. None means no
            cap.

    Returns:
        dict: Same shape as get_all but filtered. Returns an "ids" key that
            is an empty list if no records match.
    """
    if limit is None:
        return _collection().get(where=where)
    return _collection().get(where=where, limit=limit)


# ##############################################################################
# Write helper
# ##############################################################################


def add(
    ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
) -> None:
    """Insert chunks with pre-computed embeddings into the collection.

    Args:
        ids (list[str]): Chunk identifiers; must be unique within the
            collection.
        documents (list[str]): Chunk text bodies.
        embeddings (list[list[float]]): One vector per chunk, same order as
            documents.
        metadatas (list[dict]): One metadata dict per chunk, same order.

    Approach:
        Goes through the underlying chromadb.Collection's `add` method
        rather than `Chroma.add_documents`. The LangChain wrapper would
        invoke its `embedding_function` and re-embed every input text;
        since the ingest pipeline has already computed embeddings, the
        raw add lets us pass them in directly and avoid the wasted
        SPECTER2 pass.
    """
    _collection().add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
