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
