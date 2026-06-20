"""Configuration for the paper-sourcing scripts."""

# arXiv categories to fetch from.
# Full taxonomy: https://arxiv.org/category_taxonomy
CATEGORIES = [
    "cs.AI",    # Artificial Intelligence
    "cs.LG",    # Machine Learning
    "cs.CL",    # Computation and Language (NLP)
    "cs.CV",    # Computer Vision
    "cs.IR",    # Information Retrieval
    "stat.ML",  # Machine Learning (statistical methods)
]

# Maximum number of results to fetch from arXiv per run, before filtering.
MAX_RESULTS = 50

# Only download papers submitted in the last N days.
DATE_DAYS = 30

# Optional keyword filter; empty list = no keyword constraint.
# Each keyword adds an AND clause against the paper's full-text fields.
KEYWORDS = []  # e.g. ["retrieval augmented generation"]

# --- Paths ---
# Relative paths resolve from this config file's directory (scripts/sourcing/);
# absolute paths are used as-is.
#
# PAPERS_DIR is where downloaded PDFs land. Default "../../docs" points at
# the project's docs/ directory, which is what tools/ingest.py reads. If you
# change PAPERS_DIR, also update DOCS_DIR in the project's main config.py to
# keep ingestion aligned.
PAPERS_DIR = "../../docs"

# Path to the deduplication manifest. Default keeps it co-located with the
# script as script state, separate from the corpus itself.
MANIFEST_PATH = "manifest.json"
