# ##############################################################################
# File: parsing.py
# Purpose: Parse step and quality gates. Reads a PDF into a DoclingDocument and
#          inspects the parsed output for signs of bad extraction before the
#          rest of the pipeline runs.
#
# Contents:
#   Functions:
#     _get_converter()         - Lazy-init module-level Docling converter
#     parse_document()         - Parse a PDF via Docling (routing point reserved)
#     quality_check()          - Inspect parsed text for bad extraction
# ##############################################################################


# Standard library
import re
from pathlib import Path
from typing import Optional

# Third-party
# Docling and langdetect imports are deferred to runtime inside the functions
# that need them, so the module can be imported without those packages being
# installed (e.g. when only the agent's search tool is being used).

# Local
from config import (
    INGEST_QC_MIN_CHARS,
    INGEST_QC_MIN_ALNUM_RATIO,
    INGEST_QC_EXPECTED_LANGUAGE,
    INGEST_QC_STRUCTURE_MARKERS,
    INGEST_QC_MIN_ABSTRACT_OVERLAP,
)


# ##############################################################################
# Parsing
# ##############################################################################


# Module-level singleton. Building DocumentConverter loads the layout model
# (~770 weights) and RapidOCR's three sub-models (det, cls, rec) which together
# take ~5-6 sec. Constructing one per call meant re-paying that cost on every
# PDF; lifting it to module scope means we pay it once per process.
_CONVERTER = None


def _get_converter():
    """Return the module-level DocumentConverter, building it on first call."""
    global _CONVERTER
    if _CONVERTER is None:
        from docling.document_converter import DocumentConverter
        _CONVERTER = DocumentConverter()
    return _CONVERTER


def parse_document(path: Path):
    """Parse a single document into a DoclingDocument.

    Args:
        path (Path): Path to the PDF on disk.

    Approach:
        Calls docling's DocumentConverter directly (not the langchain-docling
        DoclingLoader), so the downstream chunker has access to raw doc_items
        rather than a heuristically-pre-grouped chunker output. See DEVLOG
        section "Ingestion Design > Chunking" for the reasoning.

        This is the designated routing point for the future: when the system
        has to handle non-paper documents (forms, slides, scanned PDFs),
        replace the body of this function with a router that picks Docling, an
        OCR pipeline, a form parser, or a slide parser based on document type.
        The signature stays stable so callers do not change.

    Returns:
        DoclingDocument: The parsed document with structural metadata intact.
    """
    converter = _get_converter()
    result = converter.convert(str(path))
    return result.document


# ##############################################################################
# Quality check
# ##############################################################################


def quality_check(parsed_text: str, paper_meta: Optional[dict]) -> list[str]:
    """Inspect the parser output for signs of bad extraction.

    Args:
        parsed_text (str): The combined text content of the parsed document.
        paper_meta (Optional[dict]): The manifest entry for this paper, used
            for the abstract-overlap check. May be None or empty.

    Approach:
        Five cheap heuristics catch most silent parser failures: char-count
        floor, alphanumeric ratio, language detection (langdetect), expected
        paper structure markers, and abstract-overlap against the manifest's
        known abstract.

    Returns:
        list[str]: Failure reasons. Empty list means the document passed.
    """
    failures: list[str] = []

    # Empty or near-empty output
    char_count = len(parsed_text)
    if char_count < INGEST_QC_MIN_CHARS:
        failures.append(f"too_short ({char_count} chars)")
        return failures  # Other checks are meaningless on empty text

    # Alphanumeric / whitespace ratio (garbled output has low ratio)
    alnum = sum(c.isalnum() or c.isspace() for c in parsed_text)
    ratio = alnum / char_count
    if ratio < INGEST_QC_MIN_ALNUM_RATIO:
        failures.append(f"low_alnum_ratio ({ratio:.2f})")

    # Language detection (skipped if langdetect not installed)
    try:
        from langdetect import detect, DetectorFactory
        DetectorFactory.seed = 0
        lang = detect(parsed_text[:1000])
        if lang != INGEST_QC_EXPECTED_LANGUAGE:
            failures.append(f"unexpected_language ({lang})")
    except ImportError:
        pass
    except Exception:
        failures.append("language_detection_failed")

    # Expected structure markers for research papers
    text_lower = parsed_text.lower()
    has_markers = any(m in text_lower for m in INGEST_QC_STRUCTURE_MARKERS)
    if not has_markers:
        failures.append("no_paper_structure_markers")

    # Abstract overlap (corpus-specific: only runs if manifest has an abstract)
    if paper_meta and paper_meta.get("abstract"):
        abstract_words = set(re.findall(r"\w+", paper_meta["abstract"].lower()))
        text_words = set(re.findall(r"\w+", parsed_text.lower()))
        if len(abstract_words) > 0:
            overlap = len(abstract_words & text_words) / len(abstract_words)
            if overlap < INGEST_QC_MIN_ABSTRACT_OVERLAP:
                failures.append(f"abstract_overlap_low ({overlap:.2f})")

    return failures
