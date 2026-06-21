# Mini-RAG

Solo learning and portfolio project. Started as a small RAG agent for an AMD interview. Being re-scoped now as a deeper exploration of what production-grade RAG looks like, since RAG keeps coming up in job postings and a tutorial-grade agent doesn't carry weight as a portfolio piece.

The audience for the code is hiring managers who tend to discount work that visibly displays AI assistance. Writing in commits, README, and DEVLOG should read in a plain human voice and not advertise AI involvement. See `memory/user_role.md` and `memory/commit_attribution.md` for specifics.

## What this project is becoming

The first version was a tutorial-grade RAG: PyPDFLoader, fixed-size chunks, OpenAI embeddings into local Chroma, a LangChain ReAct agent with three tools. It worked on five short AMD blog posts. That was the right scope for an interview demo.

The new direction: take this all the way to a system that handles full-length research papers, with hybrid retrieval, reranking, parent-document expansion, RAGAS-measured evaluation against a golden set, and an MCP wrapper so the whole thing can be consumed as a tool by a larger agentic pipeline.

Goals in priority order:

1. Practice the parts of RAG that aren't covered in tutorials: chunking that handles complex layout, hybrid retrieval, reranking, eval discipline.
2. Encounter the pain points in RAG directly by building through them, so I understand what production-grade RAG requires.
3. Get to a state where the result could plausibly be consumed by a larger agentic pipeline at enterprise scale.
4. Have a portfolio piece that demonstrates depth.

## Current state (as of 2026-06-20)

Working:

- Agent loop wired with LangChain `create_tool_calling_agent` + `AgentExecutor`
- Three tools: `search_knowledge_tool`, `ingest_documents_tool`, `list_sources_tool`
- `RecursiveCharacterTextSplitter(500, 100)` chunking
- OpenAI `text-embedding-3-small` embeddings into local Chroma at `chroma_db/`
- Paper fetcher at `scripts/sourcing/fetch_papers.py` pulling arXiv ML/AI papers
- 50 papers in `docs/` (gitignored) from cs.AI / cs.LG / cs.CL / cs.CV / cs.IR / stat.ML, June 2026

Pending:

- LangChain stack not yet installed in `.venv`. Only `arxiv` is. Run `uv sync` to install the main deps. The project is configured for Python `>=3.13` (3.14 hits a `zstandard` wheel issue).
- Naive `PyPDFLoader + RecursiveCharacterTextSplitter` never tested against real research papers. Expected to break on layout, figures, tables, equations. This is the next thing to validate before designing the new ingestion.
- No eval set, no retrieval or generation metrics.
- No hybrid retrieval, no reranking, no parent-document expansion, no query understanding stage.
- Not yet exposed as an MCP server.

## Tech stack

Chosen and committed:

- **LangChain** for agent and chain wiring.
- **OpenAI API**: `gpt-4o-mini` for the LLM, `text-embedding-3-small` for embeddings. Cheap and reliable for prototyping. Both swappable later.
- **arxiv** Python library for the paper fetcher.

Planned but not yet integrated:

- **LangGraph** for explicit graph-state workflows when the agent gets complex enough to want one. The current ReAct loop via `create_tool_calling_agent` is fine for the current scope.

Under evaluation, decision deferred until there's an eval set to measure against:

- **Vector database**. Currently Chroma (local SQLite, zero infra). Candidates: pgvector (Postgres extension, useful for SQL co-location and transactional consistency), Qdrant, Weaviate, Milvus. The choice should be made after I can measure recall and latency on the paper corpus, not before.

Out of scope for now:

- Fine-tuning
- Self-hosted LLMs (revisit in the local-mode phase below)
- Production deployment infrastructure

## Big components on the roadmap

Roughly in priority order. Each is a separable workstream and could be the subject of a parallel session.

1. **Eval set and metrics.** Hand-craft 20 to 30 golden Q/A pairs from the paper corpus. Wire RAGAS for Recall@k and faithfulness. Highest leverage thing to build first, because without it every other change is a guess.
2. **Ingestion strategy.** Replace PyPDFLoader with Docling or LlamaParse. VLM-caption figures with surrounding context. Preserve tables as structured data. Pick a chunking strategy that respects paper structure (sections, paragraphs, figure captions). Design the metadata schema (year, doc_type, section, parent_chunk_id, access_level, etc.).
3. **Embedding strategy.** Evaluate embedding model choices. Decide on single embedding model vs. domain-specialized. Test multimodal embedding for figures.
4. **Retrieval design.** Add BM25, hybrid via RRF. Add cross-encoder reranking. Add parent-document expansion. Add metadata filtering. Add a query understanding stage (rewrite, route, optionally HyDE).
5. **Architecture.** Move from naive RAG to agentic / adaptive RAG with proper routing.
6. **MCP wrapper.** Expose the retrieval as an MCP tool so the larger agentic pipeline can consume it.
7. **Operational polish.** Tracing (Langfuse or Phoenix), cost tracking, switchable local-model option for the privacy-aware signal, simulated access control.

## Conventions

Writing voice (from `memory/user_role.md`):

- No em-dashes
- No "not X but Y" rhetorical moves
- Avoid hedge words like "genuinely", "pragmatic", "effectively"
- Use "I" for a solo project. No corporate "we".
- No over-tidy "advantage / tradeoff / future work" summary sections
- Goal: keep the user's thinking visible. Avoid the polished LLM voice on top.

Commits (from `memory/commit_attribution.md`):

- No `Co-Authored-By: Claude` trailer in this repo
- Plain commit messages: short title, optional body bullets

Code structure:

- `agent.py`, `main.py`, `config.py` at root
- `tools/` for agent-callable tools
- `scripts/` for developer utilities outside the runtime (e.g. the paper fetcher)
- `docs/` for the corpus (gitignored)
- `tests/` for smoke tests
- `chroma_db/` is the local vector DB (gitignored)

## Where things live

- **`DEVLOG.md`** is the decision narrative, organized by topic. Read this to understand why X was chosen over Y in the project's history.
- **`memory/`** contains durable user preferences and feedback. Auto-loaded each session. Read at session start.
- **Sibling Obsidian vault under "Retrieval Augmented Generation (RAG)"** has the conceptual knowledge map: spokes for Foundations, Ingestion, Query Understanding, Retrieval, Generation, RAG Architectures, Evaluation and Observability, Reliability and Operations. The map is the design reference. This repo is the concrete implementation of parts of it.
- **This file (`CLAUDE.md`)** is the session-level briefing. Keep it lean. If something gets big enough to deserve its own doc, link to it from here instead of expanding inline.

## Active work

Sessions should update this section before starting work and clear entries when work is done or paused. Keeps parallel sessions from stepping on each other.

- (None currently in flight)
