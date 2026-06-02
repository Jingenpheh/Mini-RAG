from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from config import EMBEDDING_MODEL, CHROMA_DIR, COLLECTION_NAME


def get_vector_store():
    """Get the Chroma vector store. Creates one if it doesn't exist.

    Returns:
        Chroma: The vector store object (may be empty).
    """
    # Initialize the OpenAI embedding model — used by Chroma to convert text to vectors
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    # Connect to existing Chroma store or create a new one
    # Chroma handles both cases automatically based on whether the persist directory exists
    return Chroma(
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )
