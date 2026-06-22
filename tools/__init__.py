from langchain_core.tools import tool
from tools.ingest import ingest_documents
from tools.retriever import search_knowledge, list_sources


# --- LangChain tool wrappers ---
# The @tool decorator converts each function into a LangChain Tool object.
# LangChain reads the function name, docstring, and type hints to build
# the JSON tool schema that gets sent to the LLM with every API call.
# The docstrings below are the tool descriptions the LLM reads to decide which tool to call.


@tool
def ingest_documents_tool() -> str:
    """Scan the docs/ folder and ingest any new PDF documents into the knowledge base."""
    return ingest_documents()


@tool
def search_knowledge_tool(query: str) -> str:
    """Search the research-paper knowledge base for relevant content from arXiv ML/AI papers (cs.AI, cs.LG, cs.CL, cs.CV, cs.IR, stat.ML)."""
    return search_knowledge(query)


@tool
def list_sources_tool() -> str:
    """List all documents currently in the knowledge base with chunk counts."""
    return list_sources()


# Export all tools as a list for easy import in agent.py
all_tools = [ingest_documents_tool, search_knowledge_tool, list_sources_tool]
