# `mini_rag/` - the library package

Library code for Mini-RAG. The package contains the retrieval pipeline
(`retriever.py`), the ingestion subpackage (`ingest/`), the MCP server that
exposes both to external agents (`mcp_server.py`), the shared singletons used
by both retrieval and ingestion (`utils.py`), and a deployment verifier
(`check_setup.py`). The LangChain `@tool` wrappers in `__init__.py` are
consumed by `scripts/dev_agent.py`; production consumer agents talk to the MCP
server instead.

## Files

```
mini_rag/
├── __init__.py         # LangChain @tool wrappers (search, list, ingest)
├── retriever.py        # retrieve(), search_knowledge(), list_sources()
├── utils.py            # shared embedder + vector store singletons
├── mcp_server.py       # MCP server (production interface)
├── check_setup.py      # deployment verifier: python -m mini_rag.check_setup
├── README.md           # this file
└── ingest/             # ingestion subpackage
    ├── __init__.py     # re-exports ingest_corpus, ingest_documents, ingest_one
    ├── __main__.py     # entry point for `python -m mini_rag.ingest`
    ├── orchestrator.py # ingest_one, ingest_corpus, Result, Report, CLI
    ├── parsing.py      # parse_document, quality_check
    ├── pii.py          # PII scrub stub (slot reserved for Presidio)
    ├── chunking.py     # chunk_document
    ├── embeddings.py   # embed_chunks
    ├── storage.py      # store_chunks
    └── schema.py       # Chunk dataclass + to_metadata()
```

The dev agent at `scripts/dev_agent.py` imports `mini_rag.all_tools` and runs a
LangChain ReAct loop locally. The MCP server defines its own `@mcp.tool`
functions in `mcp_server.py`. Both surfaces call the same `retrieve()` and
`ingest_documents()` underneath, so behavior stays consistent across them.

## Retrieval

`retriever.retrieve()` is the single retrieval surface. Three stages:

1. **Hybrid retrieval**: dense (SPECTER2 cosine) and BM25 each pull
   `_FUSION_TOP` (=20) candidates. Reciprocal Rank Fusion (`_RRF_K`=60) fuses
   them into one ranked list, taking the top `RERANK_TOP` (=50) into the
   rerank pool.
2. **Cross-encoder rerank**: every `(query, chunk)` pair is scored by the
   cross-encoder. Catches fine-grained signals that bi-encoder retrieval
   smears out (specific number-row intersections in tables, formula content,
   phrase-level matches inside the right paper).
3. **Final top-k**: chunks sorted by cross-encoder score, top-k returned
   (default `TOP_K`=5).

BM25 and the cross-encoder are lazy singletons inside `retriever.py`; they
build on the first `retrieve()` call from chunks already in Chroma and are
reused on subsequent calls. The dev agent and `tests/eval/run_eval.py` both
call `retrieve()` so they always test the same retrieval logic.

`search_knowledge()` and `list_sources()` are thin presentation layers on top:
`search_knowledge()` formats hits with `arxiv_id` + title + section so the
agent can cite, `list_sources()` returns per-paper chunk counts.

## Ingestion pipeline

Six stages, in order:

```
parse -> QC -> PII -> chunk -> embed -> store
```

Each stage is its own module under `mini_rag/ingest/`. All six are
implemented.

| Stage | Module | What it does |
|---|---|---|
| Parse | `parsing.parse_document` | Docling `DocumentConverter` → `DoclingDocument`. Routing point for future non-paper doc types. |
| QC | `parsing.quality_check` | Five heuristics (see below) that catch silent parser failures. |
| PII | `pii.scrub_pii` | Passthrough stub; slot reserved for Presidio. |
| Chunk | `chunking.chunk_document` | Per-doc_item chunks with merge / drop / split refinements. |
| Embed | `embeddings.embed_chunks` | SPECTER2 via the shared embedder singleton in `utils.py`. |
| Store | `storage.store_chunks` | Writes through Chroma's raw `collection.add` with pre-computed vectors to avoid re-embedding at write time. |

`parsing.parse_document` is the reserved routing point. Today it always calls
Docling. When the system needs to handle non-paper documents (forms, slides,
scanned PDFs), only this function changes; the rest of the pipeline stays
put.

## Chunking

Each docling `doc_item` becomes one chunk by default. Three refinements on
top of that:

- **Drop floor** (`CHUNK_DROP_FLOOR` chars): items smaller than this get
  dropped as noise (page numbers, single-character artifacts).
- **Merge floor** (`CHUNK_MERGE_FLOOR` chars): consecutive same-section
  same-label items below this size get merged into a single chunk. This
  coalesces front matter (title + author + affiliation) without re-grouping
  full body paragraphs.
- **Size ceiling** (`CHUNK_SIZE_CEILING` chars): items above this get split
  on sentence boundaries.

Artifact handling:

- **Formulas**: attached to the preceding chunk when extraction succeeds.
  The Docling failure marker (`formula-not-decoded`) is detected by string
  match and the formula is dropped.
- **Tables**: exported via Docling's `export_to_markdown(doc)` so row and
  column structure is preserved as text.
- **Figures**: skipped at this stage. Captions arrive as their own
  `caption` doc_items and get included in the embedding pool.

`DEVLOG.md` section 3.1 (Ingestion) has the reasoning for each choice.

## How to run ingestion

### Inspect one paper

```bash
python -m mini_rag.ingest --sample 1 --dry-run --debug
```

Processes one document end to end, skips writes to the vector store, and
writes per-stage outputs to `debug/ingestion/` so you can see what each
stage produced.

### Run on the full corpus

```bash
python -m mini_rag.ingest
```

Processes every PDF in `INGEST_CORPUS_DIR` (default `./docs`). Failures land
in `debug/ingestion/problem_documents/` with a JSONL failure report for each
one. SPECTER2 embedding on CPU is the bottleneck; expect roughly 30 minutes
on a 50-paper corpus.

### Useful flag combinations

| Goal | Flags |
|---|---|
| Inspect one paper, no DB writes | `--sample 1 --dry-run --debug` |
| Inspect first 5 papers, no DB writes | `--sample 5 --dry-run --debug` |
| Full corpus, production mode | (no flags) |
| Try against a different folder | `--corpus-dir path/to/folder` |

## Quality gates

Five heuristics catch parser failures the parser itself does not raise:

- **`too_short`**: extracted text under `INGEST_QC_MIN_CHARS` (default 200).
- **`low_alnum_ratio`**: alphanumeric + whitespace ratio under threshold.
- **`unexpected_language`**: `langdetect` reports a language different from
  `INGEST_QC_EXPECTED_LANGUAGE` (default `en`).
- **`no_paper_structure_markers`**: none of "abstract", "introduction",
  "conclusion", "references" appears in the extracted text.
- **`abstract_overlap_low`**: less than 30% of the manifest's known abstract
  vocabulary appears in the extracted text.

All thresholds are tunable in `config.py`.

## Failure handling and dedup

A failed document is moved into `debug/ingestion/problem_documents/`, with a
`<stem>_failure_report.jsonl` listing the failure reasons and a timestamp.
To re-attempt a quarantined document, move it back into `docs/` and re-run.

Dedup runs at the start of each document: if `arxiv_id` + the current
`config_hash` are already in the vector store, the document is marked
`skipped` and the loop moves on. Changing any ingestion-relevant config
value bumps the hash and forces re-ingestion. Every chunk is also stamped
with the `pipeline_commit` (git SHA of the ingestion code), so two runs
can be told apart even if config is unchanged.

## Debug output

With `--debug` set, per-stage outputs land in `debug/ingestion/`:

```
debug/ingestion/
├── 2606.20457_parsed.json       # DoclingDocument serialized
├── 2606.20457_chunks.json       # list of Chunk records produced
└── problem_documents/
    ├── 2606.99999.pdf
    └── 2606.99999_failure_report.jsonl
```

`debug/` is gitignored. Production runs (no `--debug` flag) write nothing
into it.

## MCP server

`mcp_server.py` is the production interface. It exposes four tools and five
resources over MCP stdio. Tools:

| Tool | What it does |
|---|---|
| `search_knowledge(query, k)` | Hybrid + reranked retrieval. Returns top-k chunks with `arxiv_id`, title, section, text. |
| `list_corpus()` | Inventory of ingested papers with chunk counts. |
| `ingest_new_documents()` | Scan `INGEST_CORPUS_DIR` for new PDFs and run the pipeline. |
| `ingest_from_arxiv(arxiv_id)` | Download a paper from arXiv by ID and ingest it (uses `urllib` + `certifi`). |

Resources:

| URI | Content |
|---|---|
| `eval://golden_set` | The 30-question golden eval set as JSONL |
| `eval://latest_results` | Last line of `tests/eval/results.jsonl` |
| `eval://baseline_analysis` | The v1→v5 cumulative analysis markdown |
| `eval://v4_per_question_diagnosis` | Per-question diagnosis at v4 |
| `corpus://manifest` | Inventory of ingested papers (JSON) |

Run as: `python -m mini_rag.mcp_server`. The root README has the Claude
Desktop config snippet.

## Deployment verifier

`python -m mini_rag.check_setup` runs a small checklist (env var present,
`config.py` importable, corpus dir exists, Chroma reachable, core modules
import, MCP server importable, collection chunk count) and reports
green/red per item. Useful as the first thing to run on a fresh clone or
after a config change.

## Configuration reference

All settings live in the root `config.py`. Most have env-var overrides.

| Setting | Purpose |
|---|---|
| `INGEST_CORPUS_DIR` | Where PDFs live (default `./docs`) |
| `INGEST_DEBUG_DIR` | Where debug outputs land |
| `INGEST_PROBLEM_DIR` | Where quarantined documents go |
| `INGEST_MANIFEST_PATH` | Sourcing manifest used to join intrinsic metadata |
| `INGEST_DEFAULT_SAMPLE` | Default for `--sample` flag |
| `INGEST_DEFAULT_DRY_RUN` | Default for `--dry-run` flag |
| `INGEST_DEFAULT_DEBUG` | Default for `--debug` flag |
| `INGEST_QC_*` | Quality-gate thresholds |
| `CHUNK_DROP_FLOOR` | Drop chunks below this size |
| `CHUNK_MERGE_FLOOR` | Merge consecutive same-section same-label items below this size |
| `CHUNK_SIZE_CEILING` | Split chunks above this size on sentence boundaries |
| `CHUNK_INCLUDED_LABELS` | Docling labels to keep as chunks |
| `CHUNK_FORMULA_FAILED_MARKER` | String identifying failed formula extraction |
| `EMBEDDING_MODEL` | sentence-transformers model name (default `allenai/specter2_base`) |
| `CHROMA_DIR`, `COLLECTION_NAME` | Vector store location and collection name |
| `TOP_K` | Top-k returned by `retrieve()` (default 5) |
| `RERANK_TOP` | Cross-encoder rerank pool size (default 50) |
| `CROSS_ENCODER_MODEL` | sentence-transformers cross-encoder model name |
