# ##############################################################################
# File: chunking.py
# Purpose: Convert a parsed DoclingDocument into a list of Chunk records. One
#          chunk per docling doc_item, with a small-item merge rule and a size
#          safety net. See DEVLOG > Ingestion Design > Chunking.
#
# Contents:
#   Functions:
#     chunk_document()          - Public entry point; returns list[Chunk]
#     _split_long_text()        - Sentence-boundary split for oversized chunks
# ##############################################################################


# Standard library
import re
from typing import Any, Optional

# Local
from config import (
    CHUNK_DROP_FLOOR,
    CHUNK_MERGE_FLOOR,
    CHUNK_SIZE_CEILING,
    CHUNK_INCLUDED_LABELS,
    CHUNK_FORMULA_FAILED_MARKER,
)
from mini_rag.ingest.schema import Chunk


# ##############################################################################
# Public entry point
# ##############################################################################


def chunk_document(
    doc: Any,
    arxiv_id: str,
    paper_meta: dict,
    run_meta: dict,
) -> list[Chunk]:
    """Convert a DoclingDocument into a list of Chunk records.

    Args:
        doc: The DoclingDocument returned by parse_document().
        arxiv_id (str): The paper's arxiv identifier (used to build chunk_ids).
        paper_meta (dict): Manifest entry for this paper (title, authors,
            published_at, categories, primary_category).
        run_meta (dict): Per-run metadata (pipeline_commit, config_hash,
            ingested_at).

    Approach:
        Iterates doc.iterate_items() in document order. Section headers update
        the current section context but are not emitted as chunks. Each
        content item (text, paragraph, list_item, caption, table, title)
        becomes a candidate chunk. Consecutive same-section same-label items
        under CHUNK_MERGE_FLOOR get merged. Items under CHUNK_DROP_FLOOR are
        dropped. Items over CHUNK_SIZE_CEILING are split on sentence boundaries.

        Tables are rendered as markdown (preserves 2D structure as text).
        Formulas attach to the preceding chunk when extraction succeeds; on
        failure (placeholder marker) they're dropped.

    Returns:
        list[Chunk]: Chunks in document order, ready for embedding.
    """
    from docling_core.types.doc.document import (
        SectionHeaderItem,
        TableItem,
        FormulaItem,
        TextItem,
        TitleItem,
    )

    candidates: list[dict] = []
    current_section = ""

    # Pass 1: walk doc_items, build raw candidate dicts
    for item, _level in doc.iterate_items(with_groups=False):
        # Section heading updates context; not emitted as a chunk
        if isinstance(item, SectionHeaderItem):
            current_section = (item.text or "").strip()
            continue

        # Formula: attach to previous candidate if extraction succeeded.
        # Docling's FormulaItem often has text="" while the raw extracted
        # content lives in .orig (e.g. "Aff(2) = {(A t 0 1) : A ∈ GL(2,R) ...").
        # In v1 we dropped these silently; v2 falls back to .orig so equations
        # land in the index as auxiliary content attached to the preceding
        # explanation chunk. See DEVLOG > Ingestion Design > Chunking.
        if isinstance(item, FormulaItem):
            text = (item.text or "").strip()
            if not text:
                text = (getattr(item, "orig", "") or "").strip()
            if not text or CHUNK_FORMULA_FAILED_MARKER in text:
                continue
            if candidates:
                candidates[-1]["text"] = candidates[-1]["text"] + "\n\n" + text
                # Note: we don't add 'formula' to doc_item_labels because the
                # primary embedding signal is the preceding text; the formula is
                # auxiliary context for the LLM.
            continue

        # Table: render as markdown
        if isinstance(item, TableItem):
            md = item.export_to_markdown(doc) or ""
            md = md.strip()
            if not md:
                continue
            candidates.append({
                "text": md,
                "label": "table",
                "section": current_section,
            })
            continue

        # Title / text / paragraph / list_item / caption: candidate chunk
        if isinstance(item, TextItem):
            label = getattr(item.label, "value", str(item.label))
            if label not in CHUNK_INCLUDED_LABELS:
                continue
            text = (item.text or "").strip()
            if not text:
                continue
            candidates.append({
                "text": text,
                "label": label,
                "section": current_section,
            })
            continue

        # PictureItem and everything else: skip silently. Picture captions
        # arrive as separate TextItem(label=caption) entries and get included
        # via the branch above.

    # Pass 2: merge consecutive same-section same-label items under MERGE_FLOOR
    merged: list[dict] = []
    for cand in candidates:
        if (
            merged
            and len(merged[-1]["text"]) < CHUNK_MERGE_FLOOR
            and len(cand["text"]) < CHUNK_MERGE_FLOOR
            and merged[-1]["section"] == cand["section"]
            and merged[-1]["label"] == cand["label"]
        ):
            merged[-1]["text"] = merged[-1]["text"] + "\n\n" + cand["text"]
        else:
            merged.append(dict(cand))

    # Pass 3: apply size safety net (drop tiny, split oversized)
    finalized: list[dict] = []
    for m in merged:
        text = m["text"]
        if len(text) < CHUNK_DROP_FLOOR:
            continue
        if len(text) <= CHUNK_SIZE_CEILING:
            finalized.append(m)
            continue
        # Oversized: split on sentence boundaries, carry label + section forward
        for piece in _split_long_text(text, CHUNK_SIZE_CEILING):
            finalized.append({"text": piece, "label": m["label"], "section": m["section"]})

    # Pass 4: contextualize chunk text with paper title + section heading.
    # The prefix is included in chunk.text so it ends up embedded by SPECTER2
    # and tokenized by BM25. This binds paper-level anchors (acronyms, system
    # names) to every chunk in the paper, so queries that mention the paper
    # name can find the chunks that contain the answer content even when the
    # content itself doesn't repeat the paper's name. See DEVLOG.
    paper_title = paper_meta.get("title", "")
    for f in finalized:
        prefix_parts = []
        if paper_title:
            prefix_parts.append(f"Paper: {paper_title}")
        if f["section"]:
            prefix_parts.append(f"Section: {f['section']}")
        if prefix_parts:
            f["text"] = "\n".join(prefix_parts) + "\n\n" + f["text"]

    # Pass 5: build Chunk records with full metadata
    chunks: list[Chunk] = []
    for index, item in enumerate(finalized):
        chunk_id = f"{arxiv_id}::{index:05d}"
        chunks.append(Chunk(
            chunk_id=chunk_id,
            text=item["text"],
            chunk_index=index,
            arxiv_id=arxiv_id,
            title=paper_meta.get("title", ""),
            authors=list(paper_meta.get("authors", [])),
            published_at=paper_meta.get("published", ""),
            categories=list(paper_meta.get("categories", [])),
            primary_category=paper_meta.get("primary_category", ""),
            section_heading=item["section"],
            doc_item_labels=[item["label"]],
            char_count=len(item["text"]),
            pipeline_commit=run_meta.get("pipeline_commit", ""),
            config_hash=run_meta.get("config_hash", ""),
            ingested_at=run_meta.get("ingested_at", ""),
        ))

    return chunks


# ##############################################################################
# Internals
# ##############################################################################


_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z\[\(])")


def _split_long_text(text: str, ceiling: int) -> list[str]:
    """Split text into chunks no larger than `ceiling`, preferring sentence boundaries.

    Args:
        text (str): The text to split.
        ceiling (int): Maximum size per output piece.

    Approach:
        Splits on sentence-end punctuation followed by whitespace and a capital
        letter or opening bracket. Greedily accumulates sentences into pieces
        up to the ceiling. If a single sentence exceeds the ceiling (very long
        running text with no punctuation), the piece is left as-is rather than
        cut mid-sentence; the eval will catch this case if it matters.

    Returns:
        list[str]: Pieces in original order.
    """
    sentences = _SENTENCE_BOUNDARY.split(text) if text else []
    if not sentences:
        return [text]

    pieces: list[str] = []
    buf = ""
    for sent in sentences:
        if not buf:
            buf = sent
            continue
        if len(buf) + 1 + len(sent) <= ceiling:
            buf = buf + " " + sent
        else:
            pieces.append(buf)
            buf = sent
    if buf:
        pieces.append(buf)
    return pieces
