# ##############################################################################
# File: utils.py
# Purpose: Shared infrastructure for both ingestion and retrieval. Holds the
#          lazy embedder singleton and the Chroma vector store accessor so the
#          embedding model loads once per process.
#
# Contents:
#   Functions:
#     get_embedder()           - Lazy-init the HuggingFace embedder singleton
#     get_vector_store()       - Connect to the Chroma collection
# ##############################################################################


# Standard library
from typing import Optional

# Third-party
from langchain_chroma import Chroma

# Local
from config import EMBEDDING_MODEL, CHROMA_DIR, COLLECTION_NAME


# ##############################################################################
# Embedder singleton
# ##############################################################################


_embedder = None


def get_embedder():
    """Return the process-wide HuggingFace embedder.

    Approach:
        Lazy-instantiates HuggingFaceEmbeddings on first call so importing
        this module doesn't trigger the model load. Subsequent calls return
        the same instance, which means the sentence-transformers model lives
        in memory once and is reused for both ingestion (embedding chunks)
        and retrieval (embedding user queries).

    Returns:
        HuggingFaceEmbeddings: A LangChain Embeddings instance.
    """
    global _embedder
    if _embedder is None:
        from langchain_huggingface import HuggingFaceEmbeddings
        _embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embedder


# ##############################################################################
# Vector store
# ##############################################################################


def get_vector_store() -> Chroma:
    """Get the Chroma vector store, connecting to the configured collection.

    Approach:
        Uses the shared embedder singleton so the same model handles query
        embedding at retrieval time as did chunk embedding at ingestion time.
        Chroma creates the persist directory and collection on first use.

    Returns:
        Chroma: A LangChain Chroma wrapper backed by `CHROMA_DIR` /
            `COLLECTION_NAME`. May be empty.
    """
    return Chroma(
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=get_embedder(),
    )
