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

## Current state (as of 2026-06-22)

Working:

- Agent loop wired with LangChain `create_tool_calling_agent` + `AgentExecutor`
- Three agent tools: `search_knowledge_tool`, `ingest_documents_tool`, `list_sources_tool`
- Paper fetcher at `scripts/sourcing/fetch_papers.py` pulling arXiv ML/AI papers
- 50 papers in `docs/` (gitignored) from cs.AI / cs.LG / cs.CL / cs.CV / cs.IR / stat.ML, June 2026
- **Ingestion pipeline** at `tools/ingest/` (subpackage): parse → QC → PII → chunk → embed → store
  - Parser: Docling via `DocumentConverter` direct (not `DoclingLoader`), routing point reserved for future doc types
  - Quality gates: five heuristics (char count, alnum ratio, language, structure markers, abstract overlap)
  - PII: passthrough stub, slot reserved for Presidio
  - Chunking: paragraph-level via doc_item iteration, small-item merge under 200 chars, drop floor 30, sentence-split above 2000
  - Artifacts: formulas attach to preceding text (or drop on placeholder), tables as markdown, figures via captions only
  - Embeddings: SPECTER2 (`allenai/specter2_base`, 768-dim) via `langchain-huggingface`, shared singleton in `tools/utils.py`
  - Storage: Chroma at `./chroma_db/`, collection `research_papers`, pre-computed vectors written via underlying collection API
  - Failure handling: quarantine folder + per-doc JSONL failure reports
  - Dedup: `arxiv_id` + `config_hash` lookup; skips re-ingest under same config
  - Versioning: every chunk stamped with `pipeline_commit` (git SHA) and `config_hash`
  - Schema: `Chunk` frozen dataclass with `to_metadata()` for Chroma compatibility
  - CLI: `python -m tools.ingest [--sample N --dry-run --debug --corpus-dir PATH]`
- Retrieval surfaces `arxiv_id`, `title`, `section_heading` in formatted hits and source listings

Pending:

- No eval set, no retrieval or generation metrics.
- No hybrid retrieval (BM25 + dense + RRF), no reranking, no parent-document expansion.
- Not yet exposed as an MCP server.
- `agent.py` system prompt and `main.py` CLI banner still say "AMD knowledge assistant" — cosmetic leftover from v1.
- VLM-captioning of figures not implemented (captions used as proxy).

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

> Note: re-prioritized for the current phase against the agentic-AI job-market angle. See "Re-scoped priorities" below for the active focus and the cut list.

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

- **`DEVLOG.md`** is the decision narrative. Structured as: project goal, summary + status (current stack, key design decisions, per-version table), design deep dives (ingestion, retrieval, evaluation, deferred decisions), v1 to v6 chronological journey, future improvements. The v1-era topical-structure DEVLOG is retained at `archive/DEVLOG.md` for reference.
- **`memory/`** contains durable user preferences and feedback. Auto-loaded each session. Read at session start.
- **Sibling Obsidian vault under "Retrieval Augmented Generation (RAG)"** has the conceptual knowledge map: spokes for Foundations, Ingestion, Query Understanding, Retrieval, Generation, RAG Architectures, Evaluation and Observability, Reliability and Operations. The map is the design reference. This repo is the concrete implementation of parts of it.
- **This file (`CLAUDE.md`)** is the session-level briefing. Keep it lean. If something gets big enough to deserve its own doc, link to it from here instead of expanding inline.

## Re-scoped priorities (2026-06-22)

After re-evaluating against the agentic-AI job-market angle, the roadmap above is re-ordered for this phase. The list below supersedes the ordering in "Big components on the roadmap" until updated. Context: callbacks for agentic-AI roles are the target. Reviewer attention is finite (5 to 10 minute repo skim), and JDs consistently name LangChain, hybrid retrieval, reranker, RAGAS, MCP. The plan optimizes for hitting those names cleanly with measured numbers and a clear iteration story, not for breadth of techniques.

### What "production-grade" means here

Not "deployed at scale". A reviewer cannot tell deployment scale from a repo. What they look for, in order:

1. Measured, not vibes. Eval set, numbers, before/after comparisons on every change.
2. Reproducible. Clone, install, run, get the same numbers.
3. Failure handling. Empty retrieval, malformed LLM output, rate limits handled deliberately.
4. Observable. Bad-answer traces show what was retrieved, reranked, fed to model.
5. Decisions documented. Why this chunk size, why this retriever.
6. Clean boundaries. Ingestion, retrieval, generation, agent layer separable and testable.
7. Cost-aware. Rough sense of tokens and dollars per query.

Out of scope: HA infra, k8s, multi-tenancy, real auth, distributed serving, on-call concerns.

One-sentence test: when something breaks, the author knows it broke, knows why, has a path to fix it. Tutorials don't.

### Priority order for this phase

1. **Validation experiment.** Run the current naive `PyPDFLoader + RecursiveCharacterTextSplitter` against 5 to 10 real arxiv papers from `docs/`. Observe what breaks (layout, multi-column, equations, tables, captions). Cheapest highest-leverage move, unlocks every downstream ingestion decision. Two days max.
2. **Eval set + RAGAS.** Hand-craft 20 to 30 golden Q/A pairs from the corpus. Wire RAGAS for Recall@k and faithfulness. Single biggest portfolio signal because most candidates skip it. Enables every later decision to be measured instead of argued.
3. **Real-paper ingestion.** Replace PyPDFLoader with Docling or LlamaParse. Chunking that respects paper structure (sections, paragraphs, captions). Metadata schema (year, section, source, parent_chunk_id).
4. **Hybrid retrieval + cross-encoder reranking.** BM25 + dense via RRF, then a reranker pass. Canonical, expected, well-bounded. Measurable lift on the eval set from step 2.
5. **MCP wrapper.** Sequenced after items 1 to 4 deliberately. The tool surface (function names, arguments, return shape) depends on what the retriever can actually do, so the RAG needs to be stable before the MCP contract is worth designing. Once in, this is the single feature that signals "agentic" to a skimming reviewer. Without it the project reads as "another RAG project". With it, it reads as a retrieval tool built to be consumed by an agent.
6. **README + writeup with story arc.** v1 (tutorial, broke on papers) -> v2 (real ingestion + eval, numbers attached) -> v3 (hybrid + rerank, lift shown) -> MCP for agent integration. The narrative is the portfolio.

Cross-cutting along the way: tracing wired in from the start (Langfuse or Phoenix), per-query cost logging, basic failure handling at component boundaries, smoke tests.

### Cut list (deprioritized, defer or document as future work)

- **Embedding model A/B evaluation.** Pick `text-embedding-3-small`, document the choice, move on. No reviewer will grill this unless applying to embeddings research.
- **Vector DB swap (Chroma to pgvector/Qdrant).** Operationally motivated, not technical-depth motivated. Chroma is fine for portfolio. Document the decision.
- **Query understanding (HyDE, rewriting, routing).** Sounds advanced, small actual impact on a single-corpus academic-paper RAG, large complexity cost.
- **Adaptive / self-correcting agentic-RAG architectures.** Looks impressive in writeups, hard to show measurable value on a small corpus, disproportionate time cost.
- **Operational polish (cost dashboards, simulated ACLs, local-model swap for privacy).** None move callback rate. Local mode is a tangent unless a target JD asks for it.

### Why this cut

- Reviewer attention is finite. They skim 6 things, not 20.
- Numbers beat breadth. "Recall@5 went 0.62 to 0.81 with BM25 + RRF" beats any technique list.
- Named-tool surface matters: LangChain, hybrid retrieval, reranker, RAGAS, MCP. JDs name these. Hitting them cleanly beats depth in unnamed areas.
- The v1 -> v2 -> v3 narrative is what makes a portfolio piece interview-ready.

### Settled decisions

- **MCP placement.** Stays after the RAG stabilizes (item 5 above, after validation, eval, ingestion, and hybrid + rerank). Reason: the MCP tool surface depends on what the retriever can do, so the contract is not worth designing until the retriever is settled.
- **ReAct vs LangGraph.** Stay on the current `create_tool_calling_agent` ReAct loop. Revisit only when the loop pushes back on explicit state. Not at ideation yet.

## Active work

Sessions should update this section before starting work and clear entries when work is done or paused. Keeps parallel sessions from stepping on each other.

- (None currently in flight)
