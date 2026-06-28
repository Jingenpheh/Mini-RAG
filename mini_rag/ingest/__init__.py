# Re-export the public surface of the ingestion subpackage so external callers
# can keep doing `from mini_rag.ingest import ingest_documents, ingest_corpus`
# without needing to know which internal module each name lives in.

from mini_rag.ingest.orchestrator import (
    ingest_corpus,
    ingest_documents,
    ingest_one,
    Report,
    Result,
)

__all__ = [
    "ingest_corpus",
    "ingest_documents",
    "ingest_one",
    "Report",
    "Result",
]
