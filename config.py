# --- LLM ---
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0

# --- Embeddings ---
# SPECTER2 base from Allen AI: 768-dim, domain-specialized for academic papers.
# Runs locally via sentence-transformers; first use downloads ~400 MB to the
# Hugging Face cache (~/.cache/huggingface/hub/). No API calls, no per-token cost.
EMBEDDING_MODEL = "allenai/specter2_base"

# --- Chunking ---
CHUNK_SIZE = 500       # characters per chunk (~100-125 tokens)
CHUNK_OVERLAP = 100    # 20% overlap to preserve context across boundaries

# --- Chroma vector store ---
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "research_papers"

# --- Retrieval ---
# Top-k chunks returned by the production retrieve() call. Set to 5 so the
# eval can compute Recall@1, Recall@3, and Recall@5 from a single retrieval
# pass without re-querying.
TOP_K = 5

# --- Paths ---
DOCS_DIR = "./docs"

# --- Ingestion ---
# Where the corpus lives. PDFs in this folder get ingested.
INGEST_CORPUS_DIR = "./docs"

# Debug output root. Per-stage subfolders live underneath.
# debug/ingestion/ holds per-stage inspection JSONs and the problem_documents/ quarantine.
INGEST_DEBUG_ROOT = "./debug"
INGEST_DEBUG_DIR = f"{INGEST_DEBUG_ROOT}/ingestion"
INGEST_PROBLEM_DIR = f"{INGEST_DEBUG_DIR}/problem_documents"

# Manifest location (produced by scripts/sourcing/fetch_papers.py)
INGEST_MANIFEST_PATH = "./scripts/sourcing/manifest.json"

# Per-run defaults (CLI flags override these)
INGEST_DEFAULT_SAMPLE = None     # None = process all documents
INGEST_DEFAULT_DRY_RUN = False
INGEST_DEFAULT_DEBUG = False

# --- Ingestion quality gates ---
# Thresholds for the quality_check heuristics. Tune after first smoke test.
INGEST_QC_MIN_CHARS = 200
INGEST_QC_MIN_ALNUM_RATIO = 0.7
INGEST_QC_EXPECTED_LANGUAGE = "en"
INGEST_QC_STRUCTURE_MARKERS = ["abstract", "introduction", "conclusion", "references"]
INGEST_QC_MIN_ABSTRACT_OVERLAP = 0.3

# --- Chunking ---
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
