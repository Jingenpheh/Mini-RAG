# ##############################################################################
# File: schema.py
# Purpose: The Chunk record. Every chunk produced by the pipeline conforms to
#          this shape, and downstream code (storage, retrieval) consumes it.
#
# Contents:
#   Classes:
#     Chunk                 - Frozen dataclass holding chunk content + metadata
# ##############################################################################


# Standard library
from dataclasses import dataclass, field, asdict


# ##############################################################################
# Chunk record
# ##############################################################################


@dataclass(frozen=True)
class Chunk:
    """One chunk record: the embeddable text plus its metadata.

    Attributes:
        chunk_id (str): Deterministic identifier, e.g. "2606.20457::00042".
        text (str): The content that gets embedded.
        chunk_index (int): Position within the document (0-based).

        arxiv_id (str): Source document's arxiv identifier.
        title (str): Paper title (from manifest).
        authors (list[str]): Author list (from manifest).
        published_at (str): ISO date string (from manifest).
        categories (list[str]): arXiv category tags (from manifest).
        primary_category (str): Primary arXiv category (from manifest).

        section_heading (str): The section this chunk belongs to.
        doc_item_labels (list[str]): Docling labels for the source doc_items
            (e.g. ["text"], ["list_item"], ["table"]). Lists hold multiple
            entries when items were merged.
        char_count (int): Length of `text` in characters.

        access_level (str): Filterable field for access control. Defaults to
            "public" since the arXiv corpus is public. Slot for future tenanted
            corpora.

        pipeline_commit (str): Git SHA of the ingestion code that produced this
            chunk.
        config_hash (str): Hash of the ingestion-relevant config values.
        ingested_at (str): ISO timestamp of the run that produced this chunk.
    """

    # Identity
    chunk_id: str
    text: str
    chunk_index: int

    # Document context (from manifest)
    arxiv_id: str
    title: str
    authors: list[str]
    published_at: str
    categories: list[str]
    primary_category: str

    # Chunk context (from parsing)
    section_heading: str
    doc_item_labels: list[str]
    char_count: int

    # Access control (slot, currently always "public")
    access_level: str = "public"

    # Versioning (auto-populated by the orchestrator)
    pipeline_commit: str = ""
    config_hash: str = ""
    ingested_at: str = ""

    def to_metadata(self) -> dict:
        """Return a Chroma-compatible metadata dict.

        Approach:
            Chroma metadata values must be primitives (str, int, float, bool),
            so list-valued fields are joined with "; ". The `text` and
            `chunk_id` fields are excluded because they're passed to Chroma as
            separate arguments (documents= and ids=).

        Returns:
            dict: Filterable metadata for the vector store record.
        """
        d = asdict(self)
        d["authors"] = "; ".join(self.authors)
        d["categories"] = "; ".join(self.categories)
        d["doc_item_labels"] = "; ".join(self.doc_item_labels)
        d.pop("text", None)
        d.pop("chunk_id", None)
        return d
