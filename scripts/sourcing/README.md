# Document Sourcing

Utility scripts for sourcing documents into the RAG knowledge base. These scripts are **outside the main RAG pipeline**: they handle data acquisition only. The RAG pipeline (`mini_rag/`) consumes whatever PDFs are present in `docs/` regardless of how they got there.

## Why outside the main pipeline?

Long-term, this RAG is intended to be exposed as an MCP tool to a larger agentic pipeline, which will be responsible for sending documents in. The fetcher here is a stop-gap for sourcing test corpora during development. When the upstream agentic pipeline takes over, this folder can stay as offline tooling or be removed entirely.

This folder lives under `scripts/` (the home for developer utilities) and writes into `docs/` (the data root the RAG actually reads from). Sourcing dependencies are isolated in a uv dependency group, so the main runtime doesn't pull them.

## Layout

```
Mini-RAG/
├── docs/                       # data the RAG ingests
│   ├── legacy/                 # earlier AMD PDF corpus, kept as smoke-test reference
│   └── *.pdf                   # active corpus (papers downloaded by fetch_papers.py)
├── config.py                   # root config; sourcing settings live under SOURCING_*
└── scripts/
    └── sourcing/               # this folder
        ├── fetch_papers.py     # arXiv downloader (discovery + eval-corpus modes)
        ├── eval_corpus.json    # lock file: exact arxiv_ids the eval set is built against
        ├── manifest.json       # dedup state (created/updated by fetch_papers.py)
        └── README.md           # this file
```

The main RAG ingestion (`python -m mini_rag.ingest`) globs PDFs at `docs/*.pdf`, which non-recursively picks up the active corpus only and does not descend into `legacy/`.

## fetch_papers.py

Downloads ML / AI research papers from arXiv into `docs/`, deduplicating against `manifest.json` so re-runs only fetch new papers. Has two modes: **discovery** (open-ended search by category and date) and **eval-corpus** (reproduce the exact set of papers the eval golden set is built against).

### Configure

Sourcing settings live in the root `config.py` under the `# --- Document sourcing ---` section. The relevant names are all prefixed `SOURCING_`:

- `SOURCING_CATEGORIES`: arXiv categories to query. Defaults to a broad ML/AI set: `cs.AI`, `cs.LG`, `cs.CL`, `cs.CV`, `cs.IR`, `stat.ML`.
- `SOURCING_MAX_RESULTS`: max papers to fetch from arXiv per run, before filtering.
- `SOURCING_DATE_DAYS`: only download papers submitted in the last N days.
- `SOURCING_KEYWORDS`: optional keyword filter; empty list disables it.
- `SOURCING_PAPERS_DIR`: output directory (resolved against the project root; defaults to `./docs`).
- `SOURCING_MANIFEST_PATH`: dedup state file (defaults to `scripts/sourcing/manifest.json`).

Full arXiv category taxonomy: https://arxiv.org/category_taxonomy

### Install dependencies

Sourcing deps live in a uv dependency group, isolated from the main RAG runtime:

```bash
uv sync --group sourcing
```

To later remove them again (e.g., for a clean runtime-only install), run `uv sync` without `--group sourcing`.

### Run: discovery mode

```bash
uv run --group sourcing python scripts/sourcing/fetch_papers.py
```

Queries arXiv by category and date, deduplicates against the manifest, downloads new PDFs into `docs/`, and rewrites the manifest at the end of the run. The exact set of papers is non-deterministic across runs because arXiv's submission stream keeps moving.

### Run: eval-corpus mode

```bash
uv run --group sourcing python scripts/sourcing/fetch_papers.py --eval-corpus
```

Downloads the exact arxiv_ids listed in `eval_corpus.json` (the 50-paper set the golden eval references). Uses arXiv's by-ID lookup so the result is deterministic. Skips papers already on disk and in the manifest. Use this on a fresh clone to reproduce the eval environment; the discovery mode above will not produce the same set.

### Behavior notes

- **Deduplication** is by canonical arXiv ID (e.g. `2403.12345`), stripping any version suffix. A paper present in the manifest is never re-downloaded, even if you delete the PDF; clear the corresponding entry from `manifest.json` if you want it re-fetched.
- **Date filter** (discovery mode only) uses the `published` timestamp returned by arXiv. Papers updated later but originally submitted earlier are filtered by the original submission date.
- **No automatic cleanup.** If you want to remove a paper, delete the PDF and the matching entry from `manifest.json` yourself.
- **Manifest write is end-of-run only.** If a download fails partway through, metadata for the in-flight session is lost (papers downloaded before the failure are on disk but not recorded). Re-run is safe: papers already on disk are not re-downloaded unless their manifest entry is also missing.
