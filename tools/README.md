# `tools/` - Ingestion and Retrieval

Code the agent calls at runtime. `tools/` is the agent-tool surface (the three
LangChain-decorated wrappers in `__init__.py`). Internals of the ingestion
pipeline live one level down under `tools/ingest/`. Retrieval stays at the
top level since it's a single small file.

## Files

```
tools/
├── __init__.py          # @tool wrappers exposed to the agent
├── retriever.py         # search_knowledge, list_sources
├── utils.py             # shared vector store handle
├── README.md            # this file
└── ingest/              # ingestion subpackage
    ├── __init__.py      # re-exports ingest_corpus, ingest_documents
    ├── __main__.py      # entry point for `python -m tools.ingest`
    ├── orchestrator.py  # ingest_one, ingest_corpus, Result, Report, CLI
    ├── parsing.py       # parse_document, quality_check
    ├── pii.py           # PII scrub stub (slot reserved)
    ├── chunking.py      # chunk_document (Phase 2)
    ├── embeddings.py    # embed_chunks (Phase 3 stub)
    ├── storage.py       # store_chunks (Phase 3 stub)
    └── schema.py        # Chunk dataclass + to_metadata()
```

The agent surface (`tools/__init__.py`) imports `ingest_documents` from the
package and re-exports it as `ingest_documents_tool`. That import path stays
stable across refactors of the internals.

## Ingestion pipeline

The pipeline runs six stages in order. Phase 1 implemented parse + QC. Phase 2
adds chunking. Embedding and storage are Phase 3.

```
parse -> QC -> PII -> chunk -> embed -> store
```

Each stage is its own module under `tools/ingest/`. Configuration lives in
`config.py` under the `# --- Ingestion ---`, `# --- Ingestion quality gates ---`,
and `# --- Chunking ---` sections.

| Stage | Module | Status |
|---|---|---|
| Parse | `parsing.parse_document` | Implemented (Docling DocumentConverter) |
| QC | `parsing.quality_check` | Implemented (5 heuristics) |
| PII | `pii.scrub_pii` | Passthrough stub |
| Chunk | `chunking.chunk_document` | Implemented (Phase 2) |
| Embed | `embeddings.embed_chunks` | Phase 3 stub |
| Store | `storage.store_chunks` | Phase 3 stub |

`parsing.parse_document` is the reserved routing point. Currently it always
calls Docling. When the system needs to handle non-paper documents (forms,
slides, scanned PDFs), only this function changes; the rest of the pipeline
stays.

## Chunking

Each docling `doc_item` becomes one chunk by default. The chunker applies
three refinements on top of that:

- **Drop floor** (`CHUNK_DROP_FLOOR` chars): items smaller than this are
  dropped as noise (page numbers, single-character artifacts).
- **Merge floor** (`CHUNK_MERGE_FLOOR` chars): consecutive same-section
  same-label items below this size get merged into a single chunk. This
  coalesces front matter (title + author + affiliation) without re-grouping
  full body paragraphs.
- **Size ceiling** (`CHUNK_SIZE_CEILING` chars): items above this get split on
  sentence boundaries.

Artifact handling:

- **Formulas**: attached to the preceding chunk when extraction succeeds. The
  failure marker (`formula-not-decoded`) is detected by string match and the
  formula is dropped.
- **Tables**: exported via Docling's `export_to_markdown(doc)` so row and
  column structure is preserved as text.
- **Figures**: skipped. Captions arrive as their own `caption` doc_items and
  get included in the embedding pool.

See DEVLOG > Ingestion Design > Chunking for the reasoning.

## How to run

### Inspect one paper

```bash
python -m tools.ingest --sample 1 --dry-run --debug
```

This processes one document end to end, skips writes to the vector store, and
writes per-stage outputs to `debug/ingestion/` so you can see what each stage
produced.

### Run on the full corpus

```bash
python -m tools.ingest
```

Processes every PDF in `docs/`. Failures are isolated to
`debug/ingestion/problem_documents/` with a JSONL failure report for each one.

### Useful flag combinations

| Goal | Flags |
|---|---|
| Inspect one paper, no DB writes | `--sample 1 --dry-run --debug` |
| Inspect first 5 papers, no DB writes | `--sample 5 --dry-run --debug` |
| Run full corpus in production mode | (no flags) |
| Try the pipeline against a different folder | `--corpus-dir path/to/other/folder` |

## Quality gates

Five heuristics catch the parser failures that the parser itself does not raise:

- **`too_short`**: extracted text under `INGEST_QC_MIN_CHARS` (default 200).
- **`low_alnum_ratio`**: alphanumeric + whitespace ratio under threshold.
- **`unexpected_language`**: `langdetect` reports a language different from
  `INGEST_QC_EXPECTED_LANGUAGE` (default `en`).
- **`no_paper_structure_markers`**: none of "abstract", "introduction",
  "conclusion", "references" appears in the extracted text.
- **`abstract_overlap_low`**: less than 30% of the manifest's known abstract
  vocabulary appears in the extracted text.

All thresholds are tunable in `config.py`.

## Failure handling

A failed document gets moved into `debug/ingestion/problem_documents/`, with a
`<stem>_failure_report.jsonl` listing the failure reasons and timestamp. To
re-attempt a quarantined document, move it back into `docs/` and re-run.

## Debug output

When `--debug` is set, per-stage outputs land in `debug/ingestion/`:

```
debug/ingestion/
├── 2606.20457_parsed.json    # DoclingDocument serialized
├── 2606.20457_chunks.json    # list of Chunk records produced
└── problem_documents/
    ├── 2606.99999.pdf
    └── 2606.99999_failure_report.jsonl
```

`debug/` is gitignored. Production runs (no `--debug` flag) write nothing into it.

## Configuration reference

Set in `config.py`:

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
