"""Quick smoke test for the ingestion pipeline."""
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from tools.ingest import ingest_documents

# First run — should ingest all PDFs
print("=== First Ingest ===")
result = ingest_documents()
print(result)

# Second run — should detect duplicates and skip
print("\n=== Second Ingest (dedup check) ===")
result = ingest_documents()
print(result)
