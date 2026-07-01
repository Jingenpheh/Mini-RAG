# Mini-RAG

[![CI](https://github.com/Jingenpheh/Mini-RAG/actions/workflows/ci.yml/badge.svg)](https://github.com/Jingenpheh/Mini-RAG/actions/workflows/ci.yml)

A research-paper retrieval system for arXiv ML/AI papers, exposed as an MCP server so external agents can use it as a tool.

The system runs a five-stage retrieval pipeline (parse → chunk → embed → hybrid retrieve → cross-encoder rerank) over a corpus of arXiv ML/AI papers and answers natural-language questions about them. It was built as a portfolio piece exploring what production-grade RAG actually requires: iterated against an eval set, measured at every change, and exposed via MCP for consumption by agents.

## Headline numbers

On a hand-crafted 30-question golden eval set drawn from the corpus:

| Metric | v1 baseline | v5 | v6 (current) | v1 → v6 |
|---|---|---|---|---|
| Recall@5 | 0.103 | 0.517 | 0.690 | 6.7x |
| MRR | 0.059 | 0.378 | 0.541 | 9.2x |
| Faithfulness (LLM-judged) | 0.634 | 0.826 | 0.876 | +0.242 |
| Context recall (LLM-judged) | 0.169 | 0.608 | 0.661 | 3.9x |
| Answer correctness (LLM-judged) | 0.267 | 0.474 | 0.505 | 1.9x |

The full v1 → v1.1 → v2 → v3 → v4 → v5 → v6 journey, including which fix targeted which failure mode, is in [DEVLOG.md](DEVLOG.md) and [tests/eval/analysis/baseline_analysis.md](tests/eval/analysis/baseline_analysis.md).

The v5 to v6 step was a BM25 tokenizer change (hyphen-aware split plus Porter stemming, adopted after an ablation study at `tests/ablation/bm25_tokenization.py`). Retrieval metrics moved strongly across the board and every RAGAS metric moved with them. An earlier v6 eval run (against an uncommitted working tree) recorded `answer_correctness` at 0.458, which was a -0.016 dip vs v5; the re-run against a clean commit produced 0.505 (+0.031 vs v5), confirming the earlier dip was LLM-judge variance. That story is kept in the DEVLOG rather than hidden.

## Stack

- **Embeddings**: SPECTER2 (Allen AI, 768-dim, paper-specialized, runs locally)
- **Vector store**: Chroma (local SQLite)
- **Parsing**: Docling (layout-aware PDF parsing with table + formula extraction)
- **Retrieval**: hybrid (BM25 + dense via Reciprocal Rank Fusion) + cross-encoder reranking
- **Chunking**: docling doc-item granularity with contextual prefix (paper title + section) prepended
- **Evaluation**: custom retrieval metrics (Recall@k, MRR, NDCG) + RAGAS (faithfulness, context precision/recall, answer correctness/relevancy)
- **Generation (LLM)**: gpt-4o-mini via OpenAI API (used only by the dev agent and eval-time generation simulator)
- **External interface**: Model Context Protocol (MCP) server

## Project structure

```
Mini-RAG/
├── README.md                       ← this file
├── DEVLOG.md                       ← decision narrative across the project
├── CLAUDE.md                       ← session briefing for AI assistants
├── config.py                       ← single source of truth for all config
├── pyproject.toml                  ← project deps
│
├── mini_rag/                       ← library code (the package)
│   ├── retriever.py                ← hybrid retrieval + cross-encoder rerank
│   ├── utils.py                    ← shared singletons (embedder, vector store)
│   ├── mcp_server.py               ← MCP server (production interface)
│   ├── check_setup.py              ← deployment verification utility
│   └── ingest/                     ← ingestion pipeline subpackage
│
├── scripts/                        ← CLI utilities (dev-time, not library code)
│   ├── dev_agent.py                ← interactive LangChain dev agent
│   └── sourcing/                   ← arXiv paper fetcher
│       └── fetch_papers.py
│
└── tests/
    └── eval/                       ← evaluation framework
        ├── run_eval.py             ← eval runner (deterministic + RAGAS metrics)
        ├── golden_set.jsonl        ← 30 hand-crafted Q/A pairs
        ├── analysis/               ← version-by-version writeups
        └── README.md
```

The `mini_rag/` package is the library. The MCP server in `mini_rag/mcp_server.py` is the production interface. `scripts/dev_agent.py` is a LangChain-based interactive REPL for local testing.

## Quick reproduce on a fresh clone

```bash
# 1) Install dependencies
uv sync

# 2) Optionally fetch the exact 50-paper eval corpus
uv run --group sourcing python scripts/sourcing/fetch_papers.py --eval-corpus

# 3) Set up your OpenAI API key
cp .env.example .env
# edit .env and add OPENAI_API_KEY

# 4) Verify the setup
python -m mini_rag.check_setup

# 5) Ingest the corpus (~30 min on CPU; SPECTER2 embedding is the bottleneck)
python -m mini_rag.ingest --debug

# 6) Run the eval to reproduce the v5 numbers
python -m tests.eval.run_eval
```

After step 5 you'll have ~7,400 chunks indexed in `chroma_db/`. After step 6 you'll see overall + per-type metrics matching the headline table above.

## Run as MCP server

The production interface is MCP. To wire Mini-RAG into Claude Desktop:

```jsonc
// ~/.config/claude/claude_desktop_config.json (Mac/Linux)
// %APPDATA%/Claude/claude_desktop_config.json (Windows)
{
  "mcpServers": {
    "mini-rag": {
      "command": "python",
      "args": ["-m", "mini_rag.mcp_server"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "INGEST_CORPUS_DIR": "/absolute/path/to/papers"
      }
    }
  }
}
```

Restart Claude Desktop and Mini-RAG's four tools and five resources will be available.

### MCP tools exposed

| Tool | Purpose |
|---|---|
| `search_knowledge(query, k)` | Hybrid + reranked retrieval. Returns top-k chunks with arxiv_id, title, section, text. |
| `list_corpus()` | Inventory of ingested papers with chunk counts. |
| `ingest_new_documents()` | Scan corpus directory for new PDFs and process them. |
| `ingest_from_arxiv(arxiv_id)` | Download a paper from arXiv by ID and ingest it. |

### MCP resources exposed

| Resource URI | Content |
|---|---|
| `eval://golden_set` | The 30-question golden eval set as JSONL |
| `eval://latest_results` | Latest eval run record (last line of results.jsonl) |
| `eval://baseline_analysis` | The v1→v5 cumulative journey analysis markdown |
| `eval://v4_per_question_diagnosis` | Per-question diagnosis at v4 |
| `corpus://manifest` | Inventory of ingested papers as JSON |

## Run as local dev agent

For interactive testing without MCP:

```bash
python -m scripts.dev_agent
```

This launches a LangChain ReAct agent with the same retrieval tools as the MCP server. Useful for sanity-checking changes locally.

## Testing

Two test rings, run independently:

- `pytest tests/unit/` runs the fast unit tests (under 10 seconds, no network, no model loads). These pin pure-function behavior: chunking rules, metadata serialization, quality-check heuristics, RRF math, sourcing helpers, and the deployment-check functions.
- `python tests/eval/run_eval.py` runs the integration eval: loads SPECTER2, parses real PDFs, hits Chroma, calls the LLM judge. Produces metrics (Recall@k, MRR, NDCG, RAGAS faithfulness / context recall / answer correctness) rather than pass/fail assertions.

There is no middle ring. A slow integration test outside the eval would add maintenance cost without producing measurement signal, so it stays out.

### What's not unit-tested, and why

- `mini_rag/mcp_server.py` is thin MCP framework wiring. Testing it meaningfully needs an MCP client to talk to it; that integration belongs with the client, not with this repo.
- `scripts/dev_agent.py` is LangChain agent wiring. Same shape: a meaningful test needs a live LLM. The dev agent exists for local interactive smoke checks, which is its own test surface.
- Real Docling parsing, real SPECTER2 embedding, real Chroma round-trip, and real arXiv API calls live in the eval ring or get mocked at the boundary in unit tests.

This split is the conscious choice. Coverage is intentionally not gated by percentage: each unit test pins a behavior that would matter if it broke, rather than reaching for a number.

## Configuration

All configurable values live in `config.py` and most support environment-variable override. Common overrides:

| Env var | Default | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | — | Required for the LLM (eval-time generation) |
| `INGEST_CORPUS_DIR` | `./docs` | Where PDFs are read from. Point at an existing collection. |
| `CHROMA_DIR` | `./chroma_db` | Where Chroma stores its data |
| `TOP_K` | `5` | Top-k results returned by `retrieve()` |
| `RERANK_TOP` | `50` | Cross-encoder rerank pool size |
| `EMBEDDING_MODEL` | `allenai/specter2_base` | sentence-transformers model name |

For runtime tuning you set these env vars; for permanent project changes you edit `config.py`.

## Where to look next

- [DEVLOG.md](DEVLOG.md): decision narrative across the whole project (architecture choices, why each fix was tried, what the eval said about each change).
- [tests/eval/analysis/baseline_analysis.md](tests/eval/analysis/baseline_analysis.md): cumulative v1→v5 evaluation journey with deltas per version.
- [tests/eval/analysis/v4_per_question_diagnosis.md](tests/eval/analysis/v4_per_question_diagnosis.md): per-question status as of v4 (pre-rerank-widening).
- [tests/eval/README.md](tests/eval/README.md): how the eval set is structured and how to reproduce.
- [CLAUDE.md](CLAUDE.md): session briefing for AI assistants working on this repo.

## License

MIT — see [LICENSE](LICENSE). The arXiv papers in `docs/` are subject to their own arXiv licenses.
