# `tools/` - Ingestion and Retrieval

Code the agent calls at runtime (retrieval, ingestion, source listing) and the standalone CLI for ingesting documents. The design behind these files lives in `DEVLOG.md` under "Ingestion Design".

## Files

```
tools/
├── __init__.py     # LangChain @tool wrappers exposed to the agent
├── ingest.py       # Ingestion pipeline (CLI + agent-callable)
├── retriever.py    # Vector search and source listing
├── utils.py        # Shared vector-store handle
└── README.md       # This file
```

## Ingestion pipeline

The pipeline runs five stages in order. Phase 1 implements the first two; the rest are stubs.

```
parse -> QC -> chunk -> embed -> store
```

Each stage is a function in `tools/ingest.py`. Configuration lives in `config.py` under the `# --- Ingestion ---` and `# --- Ingestion quality gates ---` sections.

| Stage | Function | Status |
|---|---|---|
| Parse | `parse_document(path)` | Implemented (Docling) |
| QC | `quality_check(text, meta)` | Implemented (5 heuristics) |
| Chunk | `chunk_document(parsed)` | Phase 2 stub |
| Embed | `embed_chunks(chunks)` | Phase 3 stub |
| Store | (in-line in `ingest_one`) | Phase 3 stub |

`parse_document` is the reserved routing point. Currently it always calls Docling. When the system needs to handle non-paper documents (forms, slides, scanned PDFs), only this function changes; the rest of the pipeline stays.

## How to run

### Inspect one paper

```bash
python -m tools.ingest --sample 1 --dry-run --debug
```

This processes one document end to end, skips writes to the vector store, and writes per-stage outputs to `debug/ingestion/` so you can see what each stage produced. Use this when validating that the pipeline is doing the right thing on a known-good paper.

### Run on the full corpus

```bash
python -m tools.ingest
```

Processes every PDF in `docs/`. Failures are isolated to `debug/ingestion/problem_documents/` along with a JSONL failure report for each one. A run summary prints at the end.

### Useful flag combinations

| Goal | Flags |
|---|---|
| Inspect one paper, no DB writes | `--sample 1 --dry-run --debug` |
| Inspect first 5 papers, no DB writes | `--sample 5 --dry-run --debug` |
| Run full corpus in production mode | (no flags) |
| Try the pipeline against a different folder | `--corpus-dir path/to/other/folder` |

## Quality gates

Five heuristics catch the parser failures that the parser itself does not raise:

- **`too_short`**: extracted text is under `INGEST_QC_MIN_CHARS` (default 200). Catches scanned PDFs without a text layer.
- **`low_alnum_ratio`**: ratio of alphanumeric + whitespace characters to total is below threshold. Catches garbled or encoded output.
- **`unexpected_language`**: `langdetect` reports a language different from `INGEST_QC_EXPECTED_LANGUAGE` (default `en`). Catches the wrong-language case.
- **`no_paper_structure_markers`**: none of "abstract", "introduction", "conclusion", "references" appears in the extracted text. Catches documents that are not actually research papers.
- **`abstract_overlap_low`**: less than 30% of the manifest's known abstract vocabulary appears in the extracted text. Catches parsers that returned something, but not the actual paper.

All thresholds are tunable in `config.py`.

## Failure handling

A failed document gets moved into `debug/ingestion/problem_documents/`. Co-located with the PDF is a `<stem>_failure_report.jsonl` listing the failure reasons and timestamp. Open the folder, see the document and its diagnosis next to each other.

To re-attempt a quarantined document (after fixing the underlying issue, or if it was a false alarm), move it back into `docs/` and re-run ingestion.

## Debug output

When `--debug` is set, per-stage outputs land in `debug/ingestion/`:

```
debug/ingestion/
├── 2606.20457_parsed.json       # parsed.LangChain Documents from Docling
├── 2606.20457_chunks_stub.json  # chunking is Phase 2; this is a placeholder
└── problem_documents/
    ├── 2606.99999.pdf
    └── 2606.99999_failure_report.jsonl
```

`debug/` is gitignored. Production runs (no `--debug` flag) write nothing into it.

Cleanup is a one-liner when the folder gets cluttered:

```bash
find debug/ -maxdepth 1 -mindepth 1 -mtime +7 -exec rm -rf {} +
```

## Agent-tool compatibility

The agent calls `ingest_documents()` (exposed as `ingest_documents_tool` in `__init__.py`). This wrapper runs the same `ingest_corpus()` pipeline and returns a summary string. In Phase 1 the chunking and embedding steps are stubs, so calling the agent tool does not yet add new chunks to the vector store. Phase 3 wires those steps.

## Configuration reference

Set in `config.py`:

| Setting | Purpose |
|---|---|
| `INGEST_CORPUS_DIR` | Where PDFs live (default `./docs`) |
| `INGEST_DEBUG_DIR` | Where debug outputs land (default `./debug/ingestion`) |
| `INGEST_PROBLEM_DIR` | Where quarantined documents go (default `./debug/ingestion/problem_documents`) |
| `INGEST_MANIFEST_PATH` | Sourcing manifest used to join intrinsic metadata onto chunks |
| `INGEST_DEFAULT_SAMPLE` | Default for `--sample` flag |
| `INGEST_DEFAULT_DRY_RUN` | Default for `--dry-run` flag |
| `INGEST_DEFAULT_DEBUG` | Default for `--debug` flag |
| `INGEST_QC_*` | Quality-gate thresholds |
