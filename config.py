# --- LLM ---
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0

# --- Embeddings ---
EMBEDDING_MODEL = "text-embedding-3-small"

# --- Chunking ---
CHUNK_SIZE = 500       # characters per chunk (~100-125 tokens)
CHUNK_OVERLAP = 100    # 20% overlap to preserve context across boundaries

# --- Chroma vector store ---
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "amd_knowledge"

# --- Retrieval ---
TOP_K = 4

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
