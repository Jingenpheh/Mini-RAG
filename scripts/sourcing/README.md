# Document Sourcing

Utility scripts for sourcing documents into the RAG knowledge base. These scripts are **outside the main RAG pipeline** — they handle data acquisition only. The RAG pipeline (`agent.py`, `tools/`) consumes whatever PDFs are present in `docs/` regardless of how they got there.

## Why outside the main pipeline?

Long-term, this RAG is intended to be exposed as an MCP tool to a larger agentic pipeline, which will be responsible for sending documents in. The fetcher here is a stop-gap for sourcing test corpora during development. When the upstream agentic pipeline takes over, this folder can stay as offline tooling or be removed entirely.

This folder lives under `scripts/` (the home for developer utilities) and writes into `docs/` (the data root the RAG actually reads from). Sourcing dependencies are isolated in a uv dependency group, so the main runtime doesn't pull them.

## Layout

```
Mini-RAG/
├── docs/                       # data the RAG ingests
│   ├── legacy/                 # earlier AMD PDF corpus, kept as smoke-test reference
│   └── *.pdf                   # active corpus (papers downloaded by fetch_papers.py)
└── scripts/
    └── sourcing/               # this folder
        ├── fetch_papers.py     # arXiv downloader
        ├── config.py           # script configuration
        ├── README.md           # this file
        └── manifest.json       # dedup state (created on first run)
```

The main RAG ingestion (`tools/ingest.py`) globs PDFs at `docs/*.pdf`, which non-recursively picks up the active corpus only — it does not include `legacy/`.

## fetch_papers.py

Downloads ML / AI research papers from arXiv into `docs/`, deduplicating against `manifest.json` so re-runs only fetch new papers.

### Configure

Edit [`config.py`](config.py):

- `CATEGORIES` — arXiv categories to query. Defaults to a broad ML/AI set: `cs.AI`, `cs.LG`, `cs.CL`, `cs.CV`, `cs.IR`, `stat.ML`.
- `MAX_RESULTS` — max papers to fetch from arXiv per run, before filtering.
- `DATE_DAYS` — only download papers submitted in the last N days.
- `KEYWORDS` — optional keyword filter; empty list disables it.
- `PAPERS_DIR` — output directory (default `../../docs` resolves to the project's `docs/`).
- `MANIFEST_PATH` — dedup state file (default `manifest.json` co-located with the script).

Full arXiv category taxonomy: https://arxiv.org/category_taxonomy

### Install dependencies

Sourcing deps live in a uv dependency group, isolated from the main RAG runtime:

```bash
uv sync --group sourcing
```

To later remove them again (e.g., for a clean runtime-only install), run `uv sync` without `--group sourcing`.

### Run

```bash
python scripts/sourcing/fetch_papers.py
```

Downloaded PDFs land in `docs/`. The manifest is rewritten atomically at the end of each run.

### Behavior notes

- **Deduplication** is by canonical arXiv ID (e.g. `2403.12345`), stripping any version suffix. A paper present in the manifest is never re-downloaded, even if you delete the PDF — clear the corresponding entry from `manifest.json` if you want it re-fetched.
- **Date filter** uses the `published` timestamp returned by arXiv. Papers updated later but originally submitted earlier are filtered by the original submission date.
- **No automatic cleanup.** If you want to remove a paper, delete the PDF and the matching entry from `manifest.json` yourself.
- **Manifest write is end-of-run only.** If a download fails partway through, all metadata for the in-flight session is lost (papers downloaded before the failure are on disk but not recorded). Re-run is safe — papers already on disk won't be re-downloaded unless their manifest entry is also missing.
