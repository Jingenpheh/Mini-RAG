"""Quick smoke test for the retrieval pipeline."""
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from tools.retriever import search_knowledge, list_sources

# Check what's in the store
print("=== List Sources ===")
print(list_sources())

# Test a search query
print("\n=== Search: AMD AI strategy ===")
print(search_knowledge("AMD AI strategy"))

# Test a second query to see different results
print("\n=== Search: agentic AI ===")
print(search_knowledge("agentic AI"))
