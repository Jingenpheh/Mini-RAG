# ##############################################################################
# File: bm25_tokenization.py
# Purpose: Ablation study for the BM25 tokenizer. Runs the full retrieval
#          pipeline against the 30-question golden eval set with six tokenizer
#          variants and reports per-variant Recall@k / MRR / NDCG@5, plus a
#          per-question-type breakdown, so the choice can be made on numbers
#          rather than intuition.
#
#          The `porter+hyphen` variant was adopted as the v6 production default
#          based on the results of this script (R@5 lift 0.517 -> 0.690 vs
#          baseline, no per-type regressions). The five other variants are
#          retained here for reproducibility and as the historical record.
#
# Variants tested:
#   baseline        - text.lower().split()  (pre-v6 production default)
#   porter          - + Porter stemming
#   nostop          - + English stopword removal (slight regression, dropped)
#   hyphen          - re.findall(r"\w+", text.lower()) (splits hyphens, too)
#   porter+nostop   - stemming and stopword removal
#   porter+hyphen   - stemming and hyphen split  (adopted as v6 default)
#
# Run:
#   uv sync                                    # snowballstemmer is a main dep
#   python -m tests.ablation.bm25_tokenization
#
# Output:
#   - Table printed to stdout (one row per variant, aggregate metrics)
#   - JSON results at tests/ablation/bm25_tokenization_results.json with three
#     top-level keys: "summary" (the table rows), and inside "variants" each
#     variant carries "aggregate", "by_type", and "per_question".
# ##############################################################################


# Standard library
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

# Set up project root on path so we can import mini_rag without installing it.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Third-party
import snowballstemmer  # noqa: E402

# Local
from mini_rag import retriever  # noqa: E402
from tqdm import tqdm  # noqa: E402


# ##############################################################################
# Paths
# ##############################################################################


GOLDEN_SET_PATH = PROJECT_ROOT / "tests" / "eval" / "golden_set.jsonl"
RESULTS_PATH = Path(__file__).resolve().parent / "bm25_tokenization_results.json"


# ##############################################################################
# Stopwords
# ##############################################################################

# Standard English stopword list. Hardcoded so the ablation doesn't depend on
# nltk.download('stopwords') corpora being present. List drawn from the
# canonical NLTK English stopwords set.
STOPWORDS = frozenset({
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing",
    "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
    "while", "of", "at", "by", "for", "with", "about", "against",
    "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
    "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how",
    "all", "any", "both", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than",
    "too", "very", "s", "t", "can", "will", "just", "don", "should", "now",
})


# ##############################################################################
# Tokenizer variants
# ##############################################################################


_porter = snowballstemmer.stemmer("porter")
_word_re = re.compile(r"\w+")


def tok_baseline(text: str) -> list[str]:
    """lowercase + whitespace split (pre-v6 production default)."""
    return text.lower().split()


def tok_porter(text: str) -> list[str]:
    """baseline + Porter stemming."""
    return [_porter.stemWord(t) for t in text.lower().split()]


def tok_nostop(text: str) -> list[str]:
    """baseline + drop English stopwords."""
    return [t for t in text.lower().split() if t not in STOPWORDS]


def tok_hyphen(text: str) -> list[str]:
    """Split on any non-word character (hyphens, punctuation, whitespace)."""
    return _word_re.findall(text.lower())


def tok_porter_nostop(text: str) -> list[str]:
    """Porter stemming + stopword removal."""
    return [
        _porter.stemWord(t)
        for t in text.lower().split()
        if t not in STOPWORDS
    ]


def tok_porter_hyphen(text: str) -> list[str]:
    """Porter stemming + hyphen split (adopted as the v6 production default)."""
    return [_porter.stemWord(t) for t in _word_re.findall(text.lower())]


VARIANTS = {
    "baseline":       tok_baseline,
    "porter":         tok_porter,
    "nostop":         tok_nostop,
    "hyphen":         tok_hyphen,
    "porter+nostop":  tok_porter_nostop,
    "porter+hyphen":  tok_porter_hyphen,
}


# ##############################################################################
# Metrics
# ##############################################################################


def recall_at_k(retrieved_ids: list[str], gold_ids: list[str], k: int) -> float:
    """1.0 if any gold chunk appears in the top-k retrieved ids, else 0.0."""
    if not gold_ids:
        return 0.0
    top_k = set(retrieved_ids[:k])
    return 1.0 if any(g in top_k for g in gold_ids) else 0.0


def mrr(retrieved_ids: list[str], gold_ids: list[str]) -> float:
    """Reciprocal of the rank of the first gold chunk; 0 if none retrieved."""
    if not gold_ids:
        return 0.0
    gold_set = set(gold_ids)
    for rank, cid in enumerate(retrieved_ids, 1):
        if cid in gold_set:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved_ids: list[str], gold_ids: list[str], k: int) -> float:
    """Normalized Discounted Cumulative Gain at k, binary relevance."""
    if not gold_ids:
        return 0.0
    gold_set = set(gold_ids)
    dcg = sum(
        (1.0 / math.log2(rank + 1))
        for rank, cid in enumerate(retrieved_ids[:k], 1)
        if cid in gold_set
    )
    # Ideal DCG: all gold chunks ranked at the top (up to k)
    n_relevant = min(len(gold_ids), k)
    idcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, n_relevant + 1))
    return dcg / idcg if idcg > 0 else 0.0


# ##############################################################################
# Golden set loader
# ##############################################################################


def load_golden_set() -> list[dict]:
    """Read tests/eval/golden_set.jsonl into a list of dicts."""
    if not GOLDEN_SET_PATH.exists():
        raise FileNotFoundError(
            f"Golden set not found at {GOLDEN_SET_PATH}. "
            "Run from project root, with the eval set in place."
        )
    questions = []
    with GOLDEN_SET_PATH.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            questions.append(json.loads(line))
    return questions


# ##############################################################################
# Run one variant
# ##############################################################################


def run_variant(variant_name: str, tokenizer, questions: list[dict]) -> dict:
    """Score one tokenizer variant against the full golden set.

    Approach:
        Clears the BM25 singleton so the next retrieve() call rebuilds the
        index under this variant's tokenizer. Then runs retrieve() for each
        question and aggregates retrieval metrics.

    Returns:
        dict: variant name, aggregate metrics, and per-type breakdown.
    """
    # Clear the cached BM25 index so it rebuilds with this variant's tokenizer
    retriever._bm25 = None

    per_q = []
    for q in tqdm(questions, desc=f"  {variant_name}", unit="q", leave=False):
        gold = q.get("gold_chunk_ids", [])
        # negative_no_answer entries have an empty gold list; skip metric-wise
        if not gold:
            continue
        docs = retriever.retrieve(q["question"], k=5, tokenizer=tokenizer)
        retrieved_ids = [
            getattr(d, "id", None) or d.metadata.get("chunk_id", "")
            for d in docs
        ]
        per_q.append({
            "id": q.get("id", ""),
            "type": q.get("type", "unknown"),
            "recall@1": recall_at_k(retrieved_ids, gold, 1),
            "recall@3": recall_at_k(retrieved_ids, gold, 3),
            "recall@5": recall_at_k(retrieved_ids, gold, 5),
            "mrr": mrr(retrieved_ids, gold),
            "ndcg@5": ndcg_at_k(retrieved_ids, gold, 5),
        })

    n = len(per_q)
    metrics = ("recall@1", "recall@3", "recall@5", "mrr", "ndcg@5")
    aggregate = {
        m: (sum(r[m] for r in per_q) / n if n else 0.0) for m in metrics
    }

    # Per-type aggregate: same metrics, grouped by question type
    by_type_rows: dict[str, list[dict]] = defaultdict(list)
    for r in per_q:
        by_type_rows[r["type"]].append(r)
    by_type = {
        t: {
            "n": len(rows),
            **{m: sum(r[m] for r in rows) / len(rows) for m in metrics},
        }
        for t, rows in sorted(by_type_rows.items())
    }

    return {
        "variant": variant_name,
        "n_questions": n,
        "aggregate": aggregate,
        "by_type": by_type,
        "per_question": per_q,
    }


# ##############################################################################
# Table rendering
# ##############################################################################


def render_table(results: list[dict]) -> str:
    """Format the per-variant aggregate metrics as a fixed-width table."""
    header = f"{'variant':<16}  {'R@1':>6}  {'R@3':>6}  {'R@5':>6}  {'MRR':>6}  {'NDCG@5':>7}"
    sep = "-" * len(header)
    lines = [header, sep]
    for r in results:
        a = r["aggregate"]
        lines.append(
            f"{r['variant']:<16}  "
            f"{a['recall@1']:>6.3f}  "
            f"{a['recall@3']:>6.3f}  "
            f"{a['recall@5']:>6.3f}  "
            f"{a['mrr']:>6.3f}  "
            f"{a['ndcg@5']:>7.3f}"
        )
    return "\n".join(lines)


# ##############################################################################
# Entry point
# ##############################################################################


def main() -> None:
    questions = load_golden_set()
    print(f"Loaded {len(questions)} questions from {GOLDEN_SET_PATH.name}\n")
    print("Running variants (each rebuilds BM25 once, ~1 sec at 7,500 chunks):\n")

    results = []
    for name, tokenizer in VARIANTS.items():
        result = run_variant(name, tokenizer, questions)
        results.append(result)

    print()
    print(render_table(results))
    print()

    # Top-level summary mirrors the printed table so the JSON file is readable
    # without parsing into per-question or by-type detail.
    summary = [
        {"variant": r["variant"], **r["aggregate"]} for r in results
    ]

    # Persist for later inspection or comparison
    RESULTS_PATH.write_text(
        json.dumps(
            {"summary": summary, "variants": results},
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Full results (summary + by-type + per-question): {RESULTS_PATH}")


if __name__ == "__main__":
    main()
