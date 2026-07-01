# `tests/ablation/` - Targeted ablation studies

One-off experiments that measure the retrieval impact of a single configuration
change against the same golden set the main eval uses. Outputs are
deterministic (no LLM calls, no API spend), so each run takes a minute or two.

Ablations live here rather than under `tests/unit/` because they aren't
pass/fail tests, and rather than under `tests/eval/` because they don't need
the full eval framework (RAGAS, LLM judge) and they aren't the regression
baseline.

## What's in here

- `bm25_tokenization.py` - swap the BM25 tokenizer (Porter stemming, stopword
  removal, hyphen splitting, combinations) and measure end-to-end retrieval
  deltas. The `porter+hyphen` variant was adopted as the v6 production
  default; the script is kept here as the reproducibility record.

## How to run

Each ablation script is standalone. Dependencies come in via the main
`uv sync` (snowballstemmer is a runtime dep since v6):

```bash
uv sync
python -m tests.ablation.bm25_tokenization
```

The script assumes the corpus has been ingested already (the existing
`chroma_db/` is the input). If you don't have an ingested corpus, run
`python -m mini_rag.ingest` first.

## Output

Each variant's Recall@1 / Recall@3 / Recall@5 / MRR / NDCG@5 against the
30-question golden set, printed as a table to stdout and written to
`tests/ablation/<name>_results.json`. The JSON has three views:

- `summary`: one row per variant with the aggregate metrics (mirrors the
  stdout table).
- `variants[].by_type`: per-question-type breakdown of the same metrics, used
  to verify a variant doesn't regress any type.
- `variants[].per_question`: full per-question metric record.
