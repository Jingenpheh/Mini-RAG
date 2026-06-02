import re
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import DOCS_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from tools.utils import get_vector_store


def clean_text(text):
    """Collapse whitespace and normalize line breaks from messy PDF extraction."""
    # PDF extraction often produces one-word-per-line text or excessive spacing
    # This collapses all whitespace sequences into a single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def ingest_documents():
    """Scan docs/ for new PDFs, chunk and embed any that aren't already ingested.

    Returns:
        str: Summary of what was ingested.
    """
    # 1. List all PDFs in the docs/ folder
    all_pdfs = glob.glob(f"{DOCS_DIR}/*.pdf")
    if not all_pdfs:
        return "No PDF files found in docs/ folder."

    # 2. Get vector store (creates if doesn't exist)
    store = get_vector_store()

    # 3. Check what's already ingested by reading source metadata from existing chunks
    if store._collection.count() > 0:
        metadatas = store._collection.get()["metadatas"]
        ingested_files = set(m["source"] for m in metadatas)
    else:
        ingested_files = set()

    # 4. Compare — find PDFs that exist in docs/ but not yet in the vector store
    new_pdfs = [pdf for pdf in all_pdfs if pdf not in ingested_files]

    if not new_pdfs:
        return f"All {len(all_pdfs)} documents already ingested. No new files found."

    # 5. Set up the text splitter — tries natural boundaries (paragraphs, sentences)
    #    before falling back to hard character cuts
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    # 6. Loop through new PDFs — load, clean, chunk, embed+store
    total_chunks = 0
    ingested_names = []

    for pdf_path in new_pdfs:
        # Extract text from each page of the PDF
        pages = PyPDFLoader(pdf_path).load()

        # Clean whitespace issues from PDF extraction
        for page in pages:
            page.page_content = clean_text(page.page_content)

        # Split pages into smaller chunks for embedding
        chunks = splitter.split_documents(pages)

        # Filter out empty chunks (e.g. from image-only pages)
        chunks = [c for c in chunks if c.page_content.strip()]
        if not chunks:
            continue

        # Embed chunks via OpenAI and store in Chroma (handled by add_documents)
        store.add_documents(chunks)
        total_chunks += len(chunks)
        ingested_names.append(pdf_path)

    # 7. Return summary for the agent to read
    names = ", ".join(ingested_names)
    return f"Ingested {len(ingested_names)} new document(s) ({total_chunks} chunks): {names}"
