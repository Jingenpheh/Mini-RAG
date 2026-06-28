"""Project-wide configuration for Mini-RAG.

Single source of truth for all configurable values. Modules read from here.
Most values support environment-variable override so deployments don't have
to fork this file. Pattern: os.environ.get("VAR", default).

Path constants are resolved against PROJECT_ROOT so consumers don't have to
care what the current working directory is. Relative env var overrides also
resolve against PROJECT_ROOT; absolute env var overrides pass through.
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def _resolve_path(env_var: str, default: str) -> str:
    """Resolve a path config value: env var first, then absolute against PROJECT_ROOT."""
    value = os.environ.get(env_var, default)
    p = Path(value)
    if not p.is_absolute():
        p = PROJECT_ROOT / p
    return str(p)


# ##############################################################################
# LLM
# ##############################################################################

LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")
LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "0"))


# ##############################################################################
# Embeddings
# ##############################################################################

# SPECTER2 base from Allen AI: 768-dim, domain-specialized for academic papers.
# Runs locally via sentence-transformers; first use downloads ~400 MB to the
# Hugging Face cache (~/.cache/huggingface/hub/). No API calls, no per-token cost.
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "allenai/specter2_base")


# ##############################################################################
# Chroma vector store
# ##############################################################################

CHROMA_DIR = _resolve_path("CHROMA_DIR", "./chroma_db")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "research_papers")


# ##############################################################################
# Retrieval
# ##############################################################################

# Top-k chunks returned by the production retrieve() call. Set to 5 so the
# eval can compute Recall@1, Recall@3, and Recall@5 from a single retrieval
# pass without re-querying.
TOP_K = int(os.environ.get("TOP_K", "5"))

# Cross-encoder reranking (v3+). After hybrid retrieval + RRF fusion, the top
# RERANK_TOP candidates are rescored by a cross-encoder model that sees the
# (query, chunk) pair together with cross-attention. The final top-k is taken
# from these reranked scores. Larger RERANK_TOP gives more chances to recover
# right-paper-wrong-chunk cases; cost scales linearly.
#   v3 default: 20
#   v5 (2026-06-27): widened to 50 to bring deeper-ranked chunks into the
#                    reranker's view (notably for table_numerical questions
#                    where BM25 ranks the gold table chunk in the 30-50
#                    range).
RERANK_TOP = int(os.environ.get("RERANK_TOP", "50"))
CROSS_ENCODER_MODEL = os.environ.get(
    "CROSS_ENCODER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


# ##############################################################################
# Ingestion
# ##############################################################################

# Where the corpus lives. PDFs in this folder get ingested. Set
# INGEST_CORPUS_DIR env var to point at any folder (e.g., a shared papers
# directory outside the repo) without modifying this file.
INGEST_CORPUS_DIR = _resolve_path("INGEST_CORPUS_DIR", "./docs")

# Debug output root. Per-stage subfolders live underneath.
INGEST_DEBUG_ROOT = _resolve_path("INGEST_DEBUG_ROOT", "./debug")
INGEST_DEBUG_DIR = str(Path(INGEST_DEBUG_ROOT) / "ingestion")
INGEST_PROBLEM_DIR = str(Path(INGEST_DEBUG_DIR) / "problem_documents")

# Manifest location (produced by scripts/sourcing/fetch_papers.py).
INGEST_MANIFEST_PATH = _resolve_path(
    "INGEST_MANIFEST_PATH", "./scripts/sourcing/manifest.json"
)

# Per-run defaults (CLI flags override these).
INGEST_DEFAULT_SAMPLE = None     # None = process all documents
INGEST_DEFAULT_DRY_RUN = False
INGEST_DEFAULT_DEBUG = False


# ##############################################################################
# Ingestion quality gates
# ##############################################################################

INGEST_QC_MIN_CHARS = 200
INGEST_QC_MIN_ALNUM_RATIO = 0.7
INGEST_QC_EXPECTED_LANGUAGE = "en"
INGEST_QC_STRUCTURE_MARKERS = ["abstract", "introduction", "conclusion", "references"]
INGEST_QC_MIN_ABSTRACT_OVERLAP = 0.3


# ##############################################################################
# Chunking
# ##############################################################################

# One chunk per docling doc_item, with a merge rule that combines consecutive
# same-section same-label items below CHUNK_MERGE_FLOOR. Items under
# CHUNK_DROP_FLOOR get dropped as noise. Items above CHUNK_SIZE_CEILING get
# split on sentence boundaries. See DEVLOG > Ingestion Design > Chunking.
CHUNK_DROP_FLOOR = 30        # chars; below this, drop entirely
CHUNK_MERGE_FLOOR = 200      # chars; below this, candidate for merging with neighbors
CHUNK_SIZE_CEILING = 2000    # chars; above this, split on sentence boundaries

# Docling labels we want to keep as chunk content. Other labels are either
# attached to neighbors (formula -> preceding text) or dropped (footnote,
# picture, page_header, page_footer).
CHUNK_INCLUDED_LABELS = ["text", "paragraph", "list_item", "caption", "table", "title"]

# Marker string docling emits when formula extraction fails. Used to detect
# failed formulas so they don't get embedded as junk.
CHUNK_FORMULA_FAILED_MARKER = "formula-not-decoded"

# Chunker behavior version. Bump this whenever chunking semantics change so
# the config_hash invalidates existing chunks and the dedup check forces
# re-ingestion.
#   v1 (initial): dropped formulas with empty docling text silently.
#   v2 (2026-06-25): falls back to FormulaItem.orig when text is empty,
#                    recovering formula content across the corpus.
#   v3 (2026-06-26): contextual chunking. Prepends "Paper: <title>\n
#                    Section: <section>\n\n" to each chunk's text before
#                    embedding, so paper-level anchors (acronyms, system
#                    names) are bound to every chunk's content. Addresses
#                    "wrong paper retrieved" failure mode where the gold
#                    answer chunk's text doesn't repeat the paper's name.
CHUNKER_VERSION = 3


# ##############################################################################
# Sourcing (arxiv paper fetcher in scripts/sourcing/)
# ##############################################################################

# arXiv categories to fetch from. Full taxonomy: https://arxiv.org/category_taxonomy
SOURCING_CATEGORIES = [
    "cs.AI",    # Artificial Intelligence
    "cs.LG",    # Machine Learning
    "cs.CL",    # Computation and Language (NLP)
    "cs.CV",    # Computer Vision
    "cs.IR",    # Information Retrieval
    "stat.ML",  # Machine Learning (statistical methods)
]

# Maximum number of results to fetch from arXiv per run, before filtering.
SOURCING_MAX_RESULTS = int(os.environ.get("SOURCING_MAX_RESULTS", "50"))

# Only download papers submitted in the last N days.
SOURCING_DATE_DAYS = int(os.environ.get("SOURCING_DATE_DAYS", "30"))

# Optional keyword filter; empty list = no keyword constraint.
# Each keyword adds an AND clause against the paper's full-text fields.
SOURCING_KEYWORDS = []  # e.g. ["retrieval augmented generation"]

# Where the sourcing script writes downloaded PDFs. Same as INGEST_CORPUS_DIR
# by default so fetched papers land where ingestion will pick them up.
SOURCING_PAPERS_DIR = _resolve_path("SOURCING_PAPERS_DIR", INGEST_CORPUS_DIR)

# Sourcing-script dedup state. Co-located with the script as throwaway state.
SOURCING_MANIFEST_PATH = _resolve_path(
    "SOURCING_MANIFEST_PATH", INGEST_MANIFEST_PATH
)