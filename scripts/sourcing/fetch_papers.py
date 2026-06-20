# ##############################################################################
# File: fetch_papers.py
# Purpose: Download ML/AI research papers from arXiv into the parent docs/
#          directory, deduplicating against a local manifest.
#
# Contents:
#   Constants:
#     SCRIPT_DIR               — Absolute path of this script's directory
#     PAPERS_DIR               — Resolved output directory (from config)
#     MANIFEST_PATH            — Resolved manifest file path (from config)
#
#   Functions:
#     _resolve()               — Resolve config path (relative or absolute)
#     load_manifest()          — Read manifest of already-downloaded papers
#     save_manifest()          — Persist manifest after updates
#     build_query()            — Compose arXiv query string from config
#     fetch_papers()           — Main entry: query, dedupe, download, update manifest
# ##############################################################################


# Standard library
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Third-party
import arxiv

# Local
# SCRIPT_DIR must be defined and added to sys.path before importing `config`,
# since the script may be invoked from any working directory.
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from config import (  # noqa: E402
    CATEGORIES,
    MAX_RESULTS,
    DATE_DAYS,
    KEYWORDS,
    PAPERS_DIR as _PAPERS_DIR_CFG,
    MANIFEST_PATH as _MANIFEST_PATH_CFG,
)


# ##############################################################################
# Path resolution
# ##############################################################################


def _resolve(p: str) -> Path:
    """Resolve a config path: absolute paths as-is, relative paths from SCRIPT_DIR."""
    path = Path(p)
    return path if path.is_absolute() else (SCRIPT_DIR / path).resolve()


PAPERS_DIR = _resolve(_PAPERS_DIR_CFG)
MANIFEST_PATH = _resolve(_MANIFEST_PATH_CFG)


# ##############################################################################
# Manifest I/O
# ##############################################################################


def load_manifest() -> dict:
    """Load the manifest of already-downloaded papers (arxiv_id → metadata)."""
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}

# ------------------------------------------------------------------------------

def save_manifest(manifest: dict) -> None:
    """Persist the manifest after updates."""
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ##############################################################################
# Query construction
# ##############################################################################


def build_query() -> str:
    """Compose the arXiv query string from CATEGORIES and KEYWORDS."""
    cat_clause = " OR ".join(f"cat:{c}" for c in CATEGORIES)
    parts = [f"({cat_clause})"]
    if KEYWORDS:
        kw_clause = " AND ".join(f'all:"{kw}"' for kw in KEYWORDS)
        parts.append(f"({kw_clause})")
    return " AND ".join(parts)


# ##############################################################################
# Main fetch routine
# ##############################################################################


def fetch_papers() -> None:
    """Query arXiv, deduplicate against the local manifest, and download new papers.

    Approach:
        Builds a category- and keyword-filtered arXiv search sorted by
        submission date (newest first). For each result, computes the
        canonical arXiv ID, skips entries already in the manifest, skips
        entries older than DATE_DAYS, downloads remaining PDFs into
        PAPERS_DIR, and records metadata in the manifest. The manifest is
        persisted once at the end.

    Returns:
        None: Side effects only — writes PDFs into PAPERS_DIR and updates
            MANIFEST_PATH; prints a per-paper progress line and a summary.
    """

    # Ensure the output directory exists and load prior state
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()

    # Compute the date cutoff and build the search query
    cutoff = datetime.now(timezone.utc) - timedelta(days=DATE_DAYS)
    query = build_query()

    print(f"Querying arXiv (categories={CATEGORIES}, last {DATE_DAYS} days, max {MAX_RESULTS})...")

    # Configure and execute the arXiv search
    search = arxiv.Search(
        query=query,
        max_results=MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )
    client = arxiv.Client()

    # Running tally of outcomes for the summary line
    new_count = 0
    skipped_dupe = 0
    skipped_old = 0

    # Process each result: dedupe, filter by date, download, record metadata
    for result in client.results(search):

        # Canonical arXiv ID (strip version suffix like "v2")
        arxiv_id = result.entry_id.rsplit("/", 1)[-1].split("v")[0]

        # Skip papers already in the manifest
        if arxiv_id in manifest:
            skipped_dupe += 1
            continue

        # Skip papers older than the configured window
        if result.published < cutoff:
            skipped_old += 1
            continue

        # Download the PDF directly from arXiv (arxiv>=4.0 dropped Result.download_pdf)
        filename = f"{arxiv_id}.pdf"
        title_preview = result.title.strip().replace("\n", " ")[:80]
        print(f"  Downloading {arxiv_id}: {title_preview}")
        urllib.request.urlretrieve(result.pdf_url, str(PAPERS_DIR / filename))

        # Record metadata for dedup + downstream ingestion use
        manifest[arxiv_id] = {
            "title": result.title.strip(),
            "authors": [str(a) for a in result.authors],
            "abstract": result.summary.strip(),
            "categories": result.categories,
            "primary_category": result.primary_category,
            "published": result.published.isoformat(),
            "updated": result.updated.isoformat(),
            "filename": filename,
        }
        new_count += 1

    # Persist the updated manifest and print the run summary
    save_manifest(manifest)

    print()
    print(f"Done. Downloaded {new_count} new paper(s).")
    print(f"Skipped {skipped_dupe} already in manifest; {skipped_old} older than {DATE_DAYS} days.")
    print(f"Manifest total: {len(manifest)} paper(s).")


if __name__ == "__main__":
    fetch_papers()
