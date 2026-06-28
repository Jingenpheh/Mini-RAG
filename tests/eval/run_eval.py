# ##############################################################################
# File: run_eval.py
# Purpose: Evaluate Mini-RAG's retrieval and (simulated) generation against the
#          hand-crafted golden set. Computes deterministic retrieval metrics
#          (Recall@k, MRR, NDCG@k) and LLM-judged RAGAS metrics in one pass.
#
# Layers tested:
#   - Retrieval: same retrieve() function the agent uses in production. Eval
#     and agent share one retrieval path so they always test the same thing.
#   - Generation (simulated): a minimal LLM call inside this script answers
#     each question from retrieved chunks. This is NOT a shipped surface; it
#     exists only to provide answers for RAGAS to score.
#
# Output:
#   - tests/eval/results.jsonl - one run record appended per invocation
#   - stdout summary table
#
# CLI:
#   python -m tests.eval.run_eval                # full eval, all questions
#   python -m tests.eval.run_eval --sample 5     # first 5 (smoke test)
#   python -m tests.eval.run_eval --no-ragas     # custom metrics only, no LLM cost
#
# Contents:
#   Functions:
#     load_golden_set()         - Read tests/eval/golden_set.jsonl
#     compute_recall_at_k()     - Deterministic Recall@k
#     compute_mrr()             - Deterministic Mean Reciprocal Rank
#     compute_ndcg_at_k()       - Deterministic NDCG@k
#     generate_answer()         - Minimal LLM call (eval-only)
#     run_ragas_metrics()       - Batch RAGAS evaluation
#     aggregate_results()       - Mean overall + per-type breakdown
#     save_run_record()         - Append run to results.jsonl
#     print_summary()           - Pretty-print summary table
#     main()                    - CLI entry point
# ##############################################################################


# Standard library
import argparse
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Third-party
from dotenv import load_dotenv

# Local
from config import LLM_MODEL, LLM_TEMPERATURE, TOP_K
from mini_rag.retriever import retrieve
from mini_rag.ingest.orchestrator import compute_pipeline_commit, compute_config_hash


# ##############################################################################
# Constants
# ##############################################################################


GOLDEN_SET_PATH = Path("tests/eval/golden_set.jsonl")
RESULTS_PATH = Path("tests/eval/results.jsonl")

EVAL_PROMPT_TEMPLATE = """Answer the question using ONLY the context below. \
If the context does not contain enough information to answer, say so explicitly.

Context:
{chunks}

Question: {question}

Answer:"""


# ##############################################################################
# Golden set loading
# ##############################################################################


def load_golden_set(path: Path = GOLDEN_SET_PATH) -> list[dict]:
    """Read the golden set from JSONL into a list of dicts."""
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


# ##############################################################################
# Deterministic retrieval metrics
# ##############################################################################


def compute_recall_at_k(retrieved_ids: list[str], gold_ids: list[str], k: int) -> Optional[float]:
    """Did any gold chunk appear in the top-k retrieved?

    Args:
        retrieved_ids (list[str]): Chunk IDs in rank order (best first).
        gold_ids (list[str]): The gold chunk IDs we expect to retrieve.
        k (int): Top-k cutoff.

    Returns:
        Optional[float]: 1.0 if any gold appears in top-k, 0.0 otherwise.
            Returns None if gold_ids is empty (negative-no-answer questions),
            so the caller can exclude from means.
    """
    if not gold_ids:
        return None
    return float(bool(set(retrieved_ids[:k]) & set(gold_ids)))


def compute_mrr(retrieved_ids: list[str], gold_ids: list[str]) -> Optional[float]:
    """Reciprocal rank of the first gold chunk in the retrieved list.

    Args:
        retrieved_ids (list[str]): Chunk IDs in rank order.
        gold_ids (list[str]): Gold chunk IDs.

    Approach:
        Rank-1 hit -> 1.0; rank-2 -> 0.5; rank-N -> 1/N; not found -> 0.0.
        Returns None if gold_ids is empty.

    Returns:
        Optional[float]: Reciprocal rank in [0, 1], or None.
    """
    if not gold_ids:
        return None
    gold_set = set(gold_ids)
    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in gold_set:
            return 1.0 / rank
    return 0.0


def compute_ndcg_at_k(retrieved_ids: list[str], gold_ids: list[str], k: int) -> Optional[float]:
    """Normalized Discounted Cumulative Gain at k.

    Args:
        retrieved_ids (list[str]): Chunk IDs in rank order.
        gold_ids (list[str]): Gold chunk IDs.
        k (int): Cutoff.

    Approach:
        Binary relevance per chunk (gold or not). DCG sums 1/log2(rank+1) for
        each gold chunk found in the top-k. Ideal DCG sums those weights for
        the ideal ordering (golds packed at the top). Score = DCG / IDCG.
        Especially informative when a question has multiple gold chunks.

    Returns:
        Optional[float]: NDCG in [0, 1], or None for empty gold_ids.
    """
    if not gold_ids:
        return None
    gold_set = set(gold_ids)
    dcg = 0.0
    for rank, chunk_id in enumerate(retrieved_ids[:k], start=1):
        if chunk_id in gold_set:
            dcg += 1.0 / math.log2(rank + 1)
    # Ideal DCG: golds packed at the top
    n_relevant = min(len(gold_set), k)
    idcg = sum(1.0 / math.log2(r + 1) for r in range(1, n_relevant + 1))
    if idcg == 0:
        return 0.0
    return dcg / idcg


# ##############################################################################
# Generation (eval-only, NOT a shipped surface)
# ##############################################################################


def generate_answer(question: str, docs: list, llm) -> str:
    """Produce a minimal answer from retrieved chunks for RAGAS scoring.

    Args:
        question (str): The question text.
        docs (list): Retrieved Documents.
        llm: The configured ChatOpenAI instance.

    Approach:
        Single LLM call with a deliberately minimal prompt: "answer using
        only this context". No tools, no loop, no agent. This is the
        floor of what any reasonable consumer of the RAG could do, so the
        RAGAS scores represent a lower bound on production performance.

    Returns:
        str: The generated answer.
    """
    chunks_text = "\n\n".join(d.page_content for d in docs)
    prompt = EVAL_PROMPT_TEMPLATE.format(chunks=chunks_text, question=question)
    return llm.invoke(prompt).content


# ##############################################################################
# RAGAS metrics
# ##############################################################################


def run_ragas_metrics(rows: list[dict], llm, embeddings) -> dict:
    """Run the configured RAGAS metrics on collected rows.

    Args:
        rows (list[dict]): Each row has question, ground_truth, contexts, answer.
        llm: A RAGAS-wrapped LLM (LangchainLLMWrapper).
        embeddings: A RAGAS-wrapped embedder (LangchainEmbeddingsWrapper).

    Approach:
        Builds a HuggingFace Dataset and calls ragas.evaluate() in one batch.
        Returns the per-question metric values as a dict keyed by question id.

    Returns:
        dict: Per-question dict {qid: {metric: score, ...}}.
    """
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_correctness,
        context_precision,
        context_recall,
        answer_relevancy,
    )

    dataset_rows = []
    qids = []
    for row in rows:
        qids.append(row["id"])
        dataset_rows.append({
            "question": row["question"],
            "ground_truth": row["ground_truth"],
            "contexts": row["contexts"],
            "answer": row["answer"],
        })

    dataset = Dataset.from_list(dataset_rows)
    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_correctness,
            context_precision,
            context_recall,
            answer_relevancy,
        ],
        llm=llm,
        embeddings=embeddings,
    )

    # Convert per-question scores to {qid: {metric: value}}
    df = result.to_pandas()
    per_q: dict[str, dict[str, float]] = {}
    metric_columns = [
        "faithfulness",
        "answer_correctness",
        "context_precision",
        "context_recall",
        "answer_relevancy",
    ]
    for i, qid in enumerate(qids):
        per_q[qid] = {col: _safe_float(df.iloc[i].get(col)) for col in metric_columns if col in df.columns}
    return per_q


def _safe_float(x) -> Optional[float]:
    """Convert NaN-or-None to None, otherwise return float."""
    if x is None:
        return None
    try:
        v = float(x)
        if math.isnan(v):
            return None
        return v
    except (TypeError, ValueError):
        return None


# ##############################################################################
# Aggregation
# ##############################################################################


def _mean(values) -> Optional[float]:
    """Mean of values, ignoring None entries. Returns None if all are None."""
    nums = [v for v in values if v is not None]
    if not nums:
        return None
    return sum(nums) / len(nums)


def aggregate_results(per_question: list[dict]) -> dict:
    """Compute overall and per-type means across all questions.

    Args:
        per_question (list[dict]): One dict per question, with metric keys.

    Returns:
        dict: {"overall": {metric: mean}, "by_type": {type: {metric: mean}}}.
    """
    all_metrics = set()
    for rec in per_question:
        all_metrics.update(k for k in rec.keys() if k not in ("id", "type"))

    overall = {m: _mean(rec.get(m) for rec in per_question) for m in sorted(all_metrics)}

    by_type: dict[str, dict] = defaultdict(dict)
    types_seen: dict[str, list] = defaultdict(list)
    for rec in per_question:
        types_seen[rec["type"]].append(rec)
    for type_name, records in types_seen.items():
        by_type[type_name]["n"] = len(records)
        for m in sorted(all_metrics):
            by_type[type_name][m] = _mean(rec.get(m) for rec in records)

    return {"overall": overall, "by_type": dict(by_type)}


# ##############################################################################
# Persistence
# ##############################################################################


def save_run_record(record: dict, path: Path = RESULTS_PATH) -> None:
    """Append one run record to the results JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ##############################################################################
# Summary printing
# ##############################################################################


def _fmt(v) -> str:
    """Format a metric value for the summary table."""
    if v is None:
        return "  -  "
    return f"{v:.3f}"


def print_summary(record: dict) -> None:
    """Print a compact summary table to stdout."""

    print()
    print("=" * 80)
    print(f"Eval run | {record['timestamp']}")
    print(f"  commit: {record['pipeline_commit']} | config: {record['config_hash']}")
    print(f"  questions: {record['n_questions']} | sample: {record.get('sample', 'all')}")
    print("=" * 80)

    overall = record["aggregate"]["overall"]
    print()
    print("Overall:")
    for m in sorted(overall.keys()):
        print(f"  {m:22s} : {_fmt(overall[m])}")

    by_type = record["aggregate"]["by_type"]
    if by_type:
        print()
        print("By question type:")
        # Print header with metric columns
        metric_keys = sorted(k for k in overall.keys() if k not in ("n",))
        header_metrics = [m[:14] for m in metric_keys]  # truncate for layout
        print(f"  {'type':24s} {'n':3s}  " + "  ".join(f"{h:>14s}" for h in header_metrics))
        for type_name, scores in by_type.items():
            row = f"  {type_name:24s} {scores.get('n', 0):3d}  " + "  ".join(
                f"{_fmt(scores.get(m)):>14s}" for m in metric_keys
            )
            print(row)

    print()
    print(f"Saved to {RESULTS_PATH}")
    print("=" * 80)


# ##############################################################################
# Main
# ##############################################################################


def main() -> None:
    """CLI entry point."""

    parser = argparse.ArgumentParser(
        description="Run the Mini-RAG evaluation against the golden set.",
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        help="Process only the first N questions (smoke testing).",
    )
    parser.add_argument(
        "--no-ragas",
        action="store_true",
        help="Skip RAGAS metrics (custom retrieval metrics only). Zero LLM cost.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=RESULTS_PATH,
        help="Override results output path.",
    )
    args = parser.parse_args()

    # Setup
    load_dotenv()
    started_at = datetime.now(timezone.utc)

    entries = load_golden_set()
    if args.sample is not None:
        entries = entries[: args.sample]

    if not entries:
        print("No entries to evaluate. Check tests/eval/golden_set.jsonl.")
        return

    # LLM + RAGAS wrappers (only built if needed)
    eval_llm = None
    ragas_llm = None
    ragas_embeddings = None
    if not args.no_ragas:
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from ragas.llms import LangchainLLMWrapper
        from ragas.embeddings import LangchainEmbeddingsWrapper

        eval_llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
        ragas_llm = LangchainLLMWrapper(eval_llm)
        ragas_embeddings = LangchainEmbeddingsWrapper(
            OpenAIEmbeddings(model="text-embedding-3-small")
        )

    print(f"Evaluating {len(entries)} question(s)...")
    print(f"  RAGAS: {'OFF' if args.no_ragas else 'ON'}")
    print()

    # Per-question loop
    rows_for_ragas = []
    per_question: list[dict] = []

    for entry in entries:
        question = entry["question"]
        gold_ids = entry["gold_chunk_ids"]

        # Production retrieval (same path as the agent).
        # langchain-chroma puts the Chroma collection ID on doc.id; chunk_id
        # is intentionally not duplicated into metadata (see Chunk.to_metadata).
        docs = retrieve(question, k=TOP_K)
        retrieved_ids = [getattr(d, "id", None) or d.metadata.get("chunk_id", "") for d in docs]

        # Custom metrics (deterministic)
        recall_1 = compute_recall_at_k(retrieved_ids, gold_ids, 1)
        recall_3 = compute_recall_at_k(retrieved_ids, gold_ids, 3)
        recall_5 = compute_recall_at_k(retrieved_ids, gold_ids, 5)
        mrr = compute_mrr(retrieved_ids, gold_ids)
        ndcg_5 = compute_ndcg_at_k(retrieved_ids, gold_ids, 5)

        record = {
            "id": entry["id"],
            "type": entry["type"],
            "recall@1": recall_1,
            "recall@3": recall_3,
            "recall@5": recall_5,
            "mrr": mrr,
            "ndcg@5": ndcg_5,
        }

        # Generation step + RAGAS row collection
        if not args.no_ragas:
            answer = generate_answer(question, docs, eval_llm)
            rows_for_ragas.append({
                "id": entry["id"],
                "question": question,
                "ground_truth": entry["answer"],
                "contexts": [d.page_content for d in docs],
                "answer": answer,
            })

        per_question.append(record)
        print(f"  {entry['id']:5s}  R@5={_fmt(recall_5)}  MRR={_fmt(mrr)}  NDCG@5={_fmt(ndcg_5)}  ({entry['type']})")

    # Batch RAGAS evaluation
    if not args.no_ragas and rows_for_ragas:
        print()
        print(f"Running RAGAS on {len(rows_for_ragas)} row(s)...")
        ragas_scores = run_ragas_metrics(rows_for_ragas, ragas_llm, ragas_embeddings)
        # Merge ragas scores into per_question records
        for rec in per_question:
            qid = rec["id"]
            if qid in ragas_scores:
                rec.update(ragas_scores[qid])

    # Aggregate, save, print
    aggregate = aggregate_results(per_question)
    elapsed = (datetime.now(timezone.utc) - started_at).total_seconds()
    run_record = {
        "timestamp": started_at.isoformat(),
        "pipeline_commit": compute_pipeline_commit(),
        "config_hash": compute_config_hash(),
        "n_questions": len(entries),
        "sample": args.sample,
        "ragas_enabled": not args.no_ragas,
        "elapsed_seconds": round(elapsed, 1),
        "aggregate": aggregate,
        "per_question": per_question,
    }
    save_run_record(run_record, args.out)
    print_summary(run_record)


if __name__ == "__main__":
    main()
