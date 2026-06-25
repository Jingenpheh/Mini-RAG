# Mini-RAG evaluation

Hand-crafted question/answer pairs plus the runner script that scores the
RAG against them. Drawn from the arXiv ML/AI corpus locked in
`scripts/sourcing/eval_corpus.json`.

## Files

- `golden_set.jsonl` - 30 hand-crafted Q/A entries, one record per line
- `run_eval.py` - the eval runner: retrieval metrics + RAGAS scoring
- `results.jsonl` - generated per run, one record per invocation (gitignored)
- `README.md` - this file

## Quick reproduce on a fresh clone

```bash
# 1) install dependencies (main deps include ragas + sentence-transformers)
uv sync

# 2) download the exact 50-paper corpus the eval set references
uv run --group sourcing python scripts/sourcing/fetch_papers.py --eval-corpus

# 3) ingest all 50 papers (~30 min on CPU; SPECTER2 embedding is the slow part)
python -m tools.ingest --debug

# 4) run the eval
python -m tests.eval.run_eval
```

The `--eval-corpus` flag downloads the specific arxiv_ids listed in
`scripts/sourcing/eval_corpus.json`. Without it, `fetch_papers.py` runs
open-ended discovery against arXiv categories and dates, which gives a
different set of papers each time and won't match the golden set.

## Schema: `golden_set.jsonl`

Each line is one JSON object:

```json
{
  "id": "Q01",
  "type": "specific_fact_lookup",
  "arxiv_id": "2606.20523",
  "section": "3.1 Source Data - Umbra Collection",
  "question": "What dataset did this paper use?",
  "answer": "...the gold answer text...",
  "gold_chunk_ids": ["2606.20523::00012"]
}
```

Field meanings:

- `id` - short identifier (Q01..Q30). Stable across reruns.
- `type` - category. See the typology table below.
- `arxiv_id` - source paper. For cross_paper entries, semicolon-delimited
  (e.g. `"2606.20563; 2606.20556"`).
- `section` - where the answer lives in the paper. For human verification.
- `question` - the question text we feed retrieval.
- `answer` - the gold answer text. Used by RAGAS for answer_correctness.
- `gold_chunk_ids` - chunk IDs that retrieval should return. Used for Recall@k,
  MRR, NDCG. Empty list intentional for `negative_no_answer` (no chunk should
  match).

## Question typology

| Type | Count | Tests |
|---|---|---|
| `specific_fact_lookup` | 6 | Precision retrieval, single chunk match |
| `definition` | 4 | Semantic embedding quality |
| `methodology` | 4 | Section-level retrieval |
| `table_numerical` | 3 | Table content (markdown export) |
| `equation` | 2 | Formula handling (currently a known weak point) |
| `comparison_contrast` | 3 | Multi-section synthesis within a single paper |
| `contribution_recall` | 3 | List_item / bullet retrieval |
| `cross_paper` | 2 | Multi-document retrieval |
| `negative_no_answer` | 1 | Grounding (system should refuse) |
| `vague_ambiguous` | 1 | Broad-query behavior |
| `multi_hop` | 1 | Two-step retrieval |

Total: 30.

## Metrics computed by `run_eval.py`

**Custom retrieval metrics** (deterministic, no LLM, no API cost):

- `recall@1`, `recall@3`, `recall@5` - did any gold chunk appear in top-k?
- `mrr` - reciprocal rank of the first gold chunk found
- `ndcg@5` - position-weighted score; especially informative for multi-gold
  questions

**RAGAS metrics** (LLM-judged via gpt-4o-mini):

- `faithfulness` - does the generated answer match the retrieved context (no
  hallucination)?
- `context_precision` - are the retrieved chunks actually relevant?
- `context_recall` - did retrieval find enough material to answer?
- `answer_correctness` - does the generated answer match the gold answer?
- `answer_relevancy` - does the generated answer address the question?

The generation step inside `run_eval.py` is a deliberately minimal LLM call
(no agent, no loop, no tool use) so RAGAS measures the floor of what any
reasonable consumer of the RAG could achieve. The production main agent
should do at least as well.

## CLI

```bash
# full eval, all 30 questions, with RAGAS
python -m tests.eval.run_eval

# smoke test on first 3 questions
python -m tests.eval.run_eval --sample 3

# custom retrieval metrics only (no LLM calls, no cost)
python -m tests.eval.run_eval --no-ragas

# write results elsewhere
python -m tests.eval.run_eval --out tests/eval/results_experiment.jsonl
```

Cost per full run: ~$0.10 - $0.20 on gpt-4o-mini.

## Results format

Each invocation appends one JSON record to `tests/eval/results.jsonl`:

```json
{
  "timestamp": "2026-06-24T...",
  "pipeline_commit": "fddb1f9",
  "config_hash": "c260af65",
  "n_questions": 30,
  "ragas_enabled": true,
  "elapsed_seconds": 480.3,
  "aggregate": {
    "overall": {"recall@5": 0.81, "mrr": 0.74, "faithfulness": 0.83, ...},
    "by_type": {"specific_fact_lookup": {...}, "equation": {...}, ...}
  },
  "per_question": [...]
}
```

`pipeline_commit` + `config_hash` tag each run with the system version, so
comparing two runs tells you exactly which code/config the deltas came from.

## Adding new questions

1. Pick a paper, find a piece of content worth asking about.
2. Phrase the question. Capture the exact gold answer text from the paper.
3. Run `python -m tools.ingest --sample 1 --dry-run --debug` to inspect the
   paper's chunks JSON at `debug/ingestion/<arxiv_id>_chunks.json`.
4. Note which chunk_id(s) contain the gold answer.
5. Append the entry to `golden_set.jsonl`. Update the typology table count.
