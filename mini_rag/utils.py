# ##############################################################################
# File: utils.py
# Purpose: Shared infrastructure used across ingestion, retrieval, and
#          sourcing. Holds the lazy embedder singleton, the Chroma vector
#          store accessor, and an HTTPS PDF-download helper that uses
#          certifi's CA bundle (so urllib calls don't fail with
#          CERTIFICATE_VERIFY_FAILED on Windows).
#
# Contents:
#   Functions:
#     get_embedder()           - Lazy-init the HuggingFace embedder singleton
#     get_vector_store()       - Connect to the Chroma collection
#     download_pdf()           - Download a PDF to disk using certifi's CAs
# ##############################################################################


# Standard library
import ssl
import urllib.request
from pathlib import Path

# Third-party
import certifi
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


# ##############################################################################
# PDF download
# ##############################################################################


def download_pdf(url: str, dest_path: Path) -> None:
    """Download a PDF over HTTPS using certifi's CA bundle.

    Args:
        url (str): Source URL (typically an arXiv PDF URL).
        dest_path (Path): Where to write the downloaded bytes. Parent
            directory must exist; the caller is responsible for that.

    Approach:
        Builds an SSL context backed by certifi's CA bundle on every call
        and passes it to `urllib.request.urlopen` directly. This avoids the
        process-wide `ssl._create_default_https_context` monkey-patch the
        codebase used to do, which changed SSL behavior for every library
        in the same process and depended on a private attribute of the
        stdlib `ssl` module.

        The certifi bundle exists to work around the fact that Python on
        Windows doesn't reliably find the system CA store, so urllib calls
        to arxiv.org fail with CERTIFICATE_VERIFY_FAILED. Per-call context
        injection scopes the fix to just the call that needs it.
    """
    ctx = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(url, context=ctx) as response:
        dest_path.write_bytes(response.read())
