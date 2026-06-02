# Mini-RAG: AMD Knowledge Assistant

A minimal RAG (Retrieval-Augmented Generation) agent built with LangChain, OpenAI, and ChromaDB. The agent answers questions about AMD using a knowledge base of AMD blog posts, with tool-calling capabilities for document ingestion, retrieval, and knowledge base management.

## Stack

- **LLM:** GPT-4o-mini via OpenAI API
- **Framework:** LangChain (tool-calling agent with ReAct pattern)
- **Vector Store:** ChromaDB (local, persisted to disk)
- **Embeddings:** OpenAI text-embedding-3-small
- **PDF Parsing:** PyPDFLoader

## Project Structure

```
├── config.py            # Configuration constants (model, chunk size, paths)
├── agent.py             # Agent setup, system prompt, LLM wiring
├── main.py              # Entry point — chat loop
├── tools/
│   ├── __init__.py      # LangChain tool definitions
│   ├── utils.py         # Shared utilities (vector store connection)
│   ├── ingest.py        # PDF ingestion pipeline (load → clean → chunk → embed → store)
│   └── retriever.py     # Knowledge base search and source listing
├── tests/
│   ├── test_ingest.py   # Ingestion smoke test
│   └── test_retriever.py# Retrieval smoke test
├── docs/                # PDF corpus (AMD blog posts)
└── DEVLOG.md            # Development log — decisions, issues, and design rationale
```

## Agent Tools

| Tool | Description |
|------|-------------|
| `search_knowledge_tool` | Searches the vector store for relevant chunks (top-k=4) |
| `ingest_documents_tool` | Scans `docs/` for new PDFs, chunks and embeds them into ChromaDB |
| `list_sources_tool` | Lists all ingested documents with chunk counts |

## Setup

```bash
# Create virtual environment (Python 3.12 recommended)
uv venv --python 3.12
source .venv/Scripts/activate  # Windows/Git Bash

# Install dependencies
uv pip install -r requirements.txt

# Set up API key
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

```bash
python main.py
```

```
AMD Knowledge Assistant (type 'quit' to exit)
==================================================

You: What is AMD's AI strategy?
Assistant: According to the "Transforming AMD with AI" blog (page 1), AMD's internal
adoption of AI is a strategic transformation...

You: What documents do you have?
Assistant: Knowledge base: 5 document(s), 78 chunks total...
```

## Development Log

[DEVLOG.md](DEVLOG.md) documents the decisions, issues, and thought process behind building this project — from chunking strategy and document parsing challenges to system prompt iteration and ideas for future improvements. It covers:

- Architecture decisions and project structure rationale
- RAG system design: chunking methods evaluated, corrective RAG considerations, document parsing issues encountered
- Agent design: ReAct pattern, MCP considerations, how LangChain wires tools to the LLM
- System prompt iteration (3 versions: too loose → too strict → balanced)
- Future directions: semantic chunking, document preprocessing agent, re-ranking, evaluation framework
