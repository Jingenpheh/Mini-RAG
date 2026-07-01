# ##############################################################################
# File: orchestrator.py
# Purpose: Ingestion orchestrator. Walks the corpus directory, runs each
#          document through the parse -> QC -> PII -> chunk -> embed -> store
#          stages, isolates failures to a quarantine folder, and prints a
#          run summary.
#
# Pipeline order:
#   parse_document -> quality_check -> scrub_pii -> chunk_document
#       -> embed_chunks -> store_chunks
#
# Contents:
#   Classes:
#     Result                  - Outcome of processing one document
#     Report                  - Summary of a full ingestion run
#
#   Functions:
#     load_manifest()         - Read arxiv_id -> metadata mapping
#     handle_failure()        - Move document to quarantine + write JSONL report
#     save_debug()            - Write per-stage output JSON for inspection
#     compute_config_hash()   - 8-char hash of ingestion-relevant config
#     compute_pipeline_commit() - Git SHA of the ingestion code
#     already_ingested()      - Dedup check against the vector store (stub)
#     ingest_one()            - Process one document end to end
#     ingest_corpus()         - Loop over corpus, return Report
#     ingest_documents()      - Wrapper used by the agent tool
#     main()                  - CLI entry point
# ##############################################################################


# Standard library
import argparse
import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# Third-party
from tqdm import tqdm

# Local
from config import (
    INGEST_CORPUS_DIR,
    INGEST_DEBUG_DIR,
    INGEST_PROBLEM_DIR,
    INGEST_MANIFEST_PATH,
    INGEST_DEFAULT_SAMPLE,
    INGEST_DEFAULT_DRY_RUN,
    INGEST_DEFAULT_DEBUG,
)
from mini_rag.ingest.parsing import parse_document, quality_check
from mini_rag.ingest.pii import scrub_pii
from mini_rag.ingest.chunking import chunk_document
from mini_rag.ingest.embeddings import embed_chunks
from mini_rag.ingest.storage import store_chunks


# ##############################################################################
# Dataclasses
# ##############################################################################


@dataclass
class Result:
    """Outcome of processing one document.

    Attributes:
        doc_path (Path): The document this Result describes.
        status (str): One of "success", "failed", "exception", "skipped".
        n_chunks (int): Number of chunks produced (0 if the document failed).
        failures (list[str]): Failure reasons if status is "failed" or "exception".
    """

    doc_path: Path
    status: str
    n_chunks: int = 0
    failures: list[str] = field(default_factory=list)

    @classmethod
    def success(cls, path: Path, n_chunks: int) -> "Result":
        return cls(doc_path=path, status="success", n_chunks=n_chunks)

    @classmethod
    def failure(cls, path: Path, failures: list[str]) -> "Result":
        return cls(doc_path=path, status="failed", failures=failures)

    @classmethod
    def exception(cls, path: Path, exc: BaseException) -> "Result":
        return cls(doc_path=path, status="exception", failures=[f"exception: {type(exc).__name__}: {exc}"])

    @classmethod
    def skipped(cls, path: Path, reason: str) -> "Result":
        return cls(doc_path=path, status="skipped", failures=[reason])


@dataclass
class Report:
    """Summary of a full ingestion run."""

    started_at: datetime
    results: list[Result] = field(default_factory=list)

    def add(self, result: Result) -> None:
        self.results.append(result)

    @property
    def successes(self) -> list[Result]:
        return [r for r in self.results if r.status == "success"]

    @property
    def failures(self) -> list[Result]:
        return [r for r in self.results if r.status in ("failed", "exception")]

    @property
    def skipped(self) -> list[Result]:
        return [r for r in self.results if r.status == "skipped"]

    def print_summary(self) -> None:
        """Print a one-screen summary of the run."""

        # Compute counts
        n_total = len(self.results)
        n_success = len(self.successes)
        n_failed = len(self.failures)
        n_skipped = len(self.skipped)
        total_chunks = sum(r.n_chunks for r in self.successes)
        elapsed = datetime.now(timezone.utc) - self.started_at

        # Print summary block
        print()
        print(f"Ingestion run {self.started_at.isoformat()}")
        print(f"  Elapsed:    {elapsed.total_seconds():.1f}s")
        print(f"  Processed:  {n_total} documents")
        print(f"  Successful: {n_success} ({total_chunks} chunks)")
        if n_skipped:
            print(f"  Skipped:    {n_skipped} (already ingested under current config)")
        print(f"  Failed:     {n_failed}")
        if n_failed:
            print(f"  See {INGEST_PROBLEM_DIR}/ for problem documents and reports.")


# ##############################################################################
# Manifest
# ##############################################################################


def load_manifest() -> dict:
    """Load the arxiv_id -> metadata manifest produced by the fetcher.

    Returns:
        dict: arxiv_id -> metadata dict. Empty dict if the manifest is missing.
    """
    path = Path(INGEST_MANIFEST_PATH)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


# ##############################################################################
# Failure handling
# ##############################################################################


def handle_failure(doc_path: Path, failures: list[str]) -> None:
    """Move a failed document to quarantine and write a co-located JSONL report.

    Args:
        doc_path (Path): The document that failed.
        failures (list[str]): The failure reasons from quality_check or an
            exception trace.

    Approach:
        Both the PDF and its <stem>_failure_report.jsonl land together in
        debug/ingestion/problem_documents/. Opening the folder shows the
        document and its diagnosis side by side. If the document was already
        quarantined from a previous run, append a new report line instead of
        moving again.
    """

    # Ensure the quarantine directory exists
    problem_dir = Path(INGEST_PROBLEM_DIR)
    problem_dir.mkdir(parents=True, exist_ok=True)

    # Append a JSONL entry recording this failure event
    report_file = problem_dir / f"{doc_path.stem}_failure_report.jsonl"
    log_entry = {
        "doc_path": str(doc_path),
        "filename": doc_path.name,
        "failures": failures,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with report_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # Move the document into quarantine; handle the "already quarantined" case
    dest = problem_dir / doc_path.name
    if dest.exists():
        # The file is already in quarantine from an earlier run. Remove the
        # duplicate at the source location instead of overwriting.
        if doc_path.resolve() != dest.resolve():
            doc_path.unlink(missing_ok=True)
    else:
        doc_path.rename(dest)


# ##############################################################################
# Debug helpers
# ##############################################################################


def save_debug(debug_dir: Path, stem: str, stage: str, data: Any) -> None:
    """Write per-stage output as JSON for inspection.

    Args:
        debug_dir (Path): The folder to write into.
        stem (str): Document identifier (e.g. arxiv_id).
        stage (str): Stage name ("parsed", "chunks", etc).
        data: The object to serialize. Best-effort conversion to JSON.
    """

    # Ensure the folder exists
    debug_dir.mkdir(parents=True, exist_ok=True)
    out_file = debug_dir / f"{stem}_{stage}.json"

    # Convert objects to something JSON-serializable
    if isinstance(data, list):
        serializable = [_to_dict(item) for item in data]
    elif isinstance(data, (dict, str, int, float, bool)) or data is None:
        serializable = data
    else:
        serializable = _to_dict(data)

    # Write
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)


def _to_dict(obj: Any) -> Any:
    """Best-effort conversion of arbitrary objects to JSON-serializable shapes."""
    # Prefer mode="json" for pydantic models (handles AnyUrl, datetime, etc.)
    if hasattr(obj, "model_dump"):
        try:
            return obj.model_dump(mode="json")
        except TypeError:
            return obj.model_dump()
    if hasattr(obj, "dict") and callable(obj.dict):
        return obj.dict()
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    return str(obj)


# ##############################################################################
# Versioning and dedup
# ##############################################################################


def compute_config_hash() -> str:
    """Compute an 8-character hash of the ingestion-relevant config values.

    Approach:
        Hashes the JSON-serialized values that affect what chunks look like.
        When any of these change, the hash changes, which lets
        already_ingested() distinguish chunks ingested under one config from
        chunks ingested under another.

    Returns:
        str: First 8 hex chars of the SHA-256.
    """
    from config import (
        EMBEDDING_MODEL,
        CHUNK_DROP_FLOOR,
        CHUNK_MERGE_FLOOR,
        CHUNK_SIZE_CEILING,
        CHUNK_INCLUDED_LABELS,
        CHUNKER_VERSION,
    )

    payload = {
        "embedding_model": EMBEDDING_MODEL,
        "chunk_drop_floor": CHUNK_DROP_FLOOR,
        "chunk_merge_floor": CHUNK_MERGE_FLOOR,
        "chunk_size_ceiling": CHUNK_SIZE_CEILING,
        "chunk_included_labels": sorted(CHUNK_INCLUDED_LABELS),
        "chunker_version": CHUNKER_VERSION,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()[:8]


def compute_pipeline_commit() -> str:
    """Return the short git SHA of the ingestion code at runtime.

    Approach:
        Runs `git rev-parse --short HEAD`. If the working copy isn't a git
        repository or git isn't available, returns "unknown".

    Returns:
        str: Short git SHA, or "unknown".
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    return "unknown"


def already_ingested(arxiv_id: str, config_hash: str) -> bool:
    """Check whether this document has chunks in the vector store under the current config.

    Args:
        arxiv_id (str): The document's arxiv identifier (filename stem).
        config_hash (str): The current run's config hash.

    Approach:
        Queries Chroma for chunks where metadata.arxiv_id matches AND
        metadata.config_hash matches. If any match, the document is already
        ingested under this exact config and should be skipped. A miss can
        mean the document is new OR the config changed; either way the
        pipeline re-ingests with the current settings, and the new chunks
        coexist with old ones under different config_hash values until
        manually pruned.

    Returns:
        bool: True if already ingested under the current config, else False.
    """
    from mini_rag import chroma_client

    try:
        result = chroma_client.get_where(
            where={
                "$and": [
                    {"arxiv_id": arxiv_id},
                    {"config_hash": config_hash},
                ]
            },
            limit=1,
        )
        return bool(result.get("ids"))
    except Exception:
        # If the collection doesn't exist yet or the query fails for any
        # reason, treat the doc as not ingested and let the pipeline run.
        # The store write itself will surface real persistence failures.
        return False


# ##############################################################################
# Per-document orchestrator
# ##############################################################################


def ingest_one(
    doc_path: Path,
    manifest: dict,
    run_meta: dict,
    debug_dir: Optional[Path] = None,
    dry_run: bool = False,
) -> Result:
    """Process one document through parse -> QC -> PII -> chunk -> embed -> store.

    Args:
        doc_path (Path): The PDF to ingest.
        manifest (dict): The arxiv_id -> metadata mapping for joining intrinsic
            metadata onto each chunk.
        run_meta (dict): Per-run metadata (pipeline_commit, config_hash,
            ingested_at) stamped onto every chunk this document produces.
        debug_dir (Optional[Path]): If set, per-stage outputs are written here.
        dry_run (bool): If True, the embed and store steps are skipped.

    Approach:
        Calls each stage in order. Bails out after QC if the document looks
        bad. Returns a Result the orchestrator can hand to handle_failure.

    Returns:
        Result: Per-document outcome.
    """

    # Look up the per-paper intrinsic metadata
    arxiv_id = doc_path.stem  # "2606.20563.pdf" -> "2606.20563"
    paper_meta = manifest.get(arxiv_id, {})

    # Parse
    doc = parse_document(doc_path)
    if debug_dir:
        save_debug(debug_dir, arxiv_id, "parsed", doc)

    # Get a single text blob for QC
    parsed_text = doc.export_to_markdown() if hasattr(doc, "export_to_markdown") else ""

    # Quality check (gate before chunking)
    failures = quality_check(parsed_text, paper_meta)
    if failures:
        return Result.failure(doc_path, failures)

    # PII scrubbing (passthrough in Phase 2; slot reserved)
    parsed_text = scrub_pii(parsed_text, paper_meta)

    # Chunking
    chunks = chunk_document(doc, arxiv_id, paper_meta, run_meta)
    if debug_dir:
        save_debug(debug_dir, arxiv_id, "chunks", chunks)

    # Embedding + storage (Phase 3 stubs)
    if not dry_run:
        vectors = embed_chunks(chunks)
        store_chunks(chunks, vectors)

    return Result.success(doc_path, n_chunks=len(chunks))


# ##############################################################################
# Corpus orchestrator
# ##############################################################################


def ingest_corpus(
    corpus_dir: Optional[Path] = None,
    sample: Optional[int] = None,
    dry_run: bool = False,
    debug_dir: Optional[Path] = None,
) -> Report:
    """Loop over the corpus directory, dispatch ingest_one, handle failures.

    Args:
        corpus_dir (Optional[Path]): The directory containing PDFs. Defaults
            to INGEST_CORPUS_DIR from config.py.
        sample (Optional[int]): If set, process only the first N documents.
        dry_run (bool): If True, the embed and store steps are skipped.
        debug_dir (Optional[Path]): If set, per-stage outputs are written here.

    Returns:
        Report: A summary object that can be printed with print_summary().
    """

    # Resolve corpus directory (default from config)
    corpus_dir = corpus_dir or Path(INGEST_CORPUS_DIR)
    manifest = load_manifest()
    config_hash = compute_config_hash()
    pipeline_commit = compute_pipeline_commit()

    # Per-run metadata stamped onto every chunk produced by this run
    started_at = datetime.now(timezone.utc)
    run_meta = {
        "pipeline_commit": pipeline_commit,
        "config_hash": config_hash,
        "ingested_at": started_at.isoformat(),
    }

    # Discover documents (non-recursive on purpose; legacy/ and problem/ stay out)
    docs = sorted(corpus_dir.glob("*.pdf"))
    if sample:
        docs = docs[:sample]

    # Ensure debug_dir exists if requested
    if debug_dir:
        debug_dir.mkdir(parents=True, exist_ok=True)

    report = Report(started_at=started_at)

    # Process each document; orchestrator only orchestrates. Wrapped in tqdm
    # so the caller (CLI or agent tool) sees an updating progress bar with
    # ETA instead of a wall of log lines. Per-doc status is written via
    # tqdm.write so it stacks cleanly above the bar.
    for doc_path in tqdm(docs, desc="Ingesting", unit="doc"):
        arxiv_id = doc_path.stem

        # Dedup check: skip documents already ingested under current config.
        # Phase 1 stub always returns False, so this never fires until Phase 3.
        if already_ingested(arxiv_id, config_hash):
            result = Result.skipped(doc_path, f"already ingested under config {config_hash}")
            report.add(result)
            tqdm.write(f"  {result.status:9s} {doc_path.name}")
            continue

        try:
            result = ingest_one(doc_path, manifest, run_meta, debug_dir=debug_dir, dry_run=dry_run)
            report.add(result)
            if result.status == "failed":
                handle_failure(doc_path, result.failures)
        except Exception as e:
            result = Result.exception(doc_path, e)
            report.add(result)
            handle_failure(doc_path, result.failures)

        # Per-document progress line
        tqdm.write(f"  {result.status:9s} {doc_path.name}")

    return report


# ##############################################################################
# Agent tool wrapper
# ##############################################################################


def ingest_documents() -> str:
    """Wrapper used by the agent's ingest_documents_tool.

    Approach:
        Runs the full ingest pipeline (parse, QC, chunk, embed, store) and
        returns a summary string the agent can read. Includes the skipped
        count so the agent can distinguish "already in the knowledge base"
        from "newly added" and from "failed".

    Returns:
        str: Summary string for the agent.
    """
    report = ingest_corpus()
    n_total = len(report.results)
    n_success = len(report.successes)
    n_skipped = len(report.skipped)
    n_failed = len(report.failures)
    new_chunks = sum(r.n_chunks for r in report.successes)
    parts = [f"Pipeline processed {n_total} document(s)."]
    if n_success:
        parts.append(
            f"Newly ingested: {n_success} document(s) "
            f"adding {new_chunks} chunks to the knowledge base."
        )
    if n_skipped:
        parts.append(
            f"Skipped: {n_skipped} document(s) already ingested under the current config."
        )
    if n_failed:
        parts.append(f"Quarantined: {n_failed} document(s) (see problem_documents/).")
    if not n_success and not n_failed:
        parts.append("No new documents needed ingesting.")
    return " ".join(parts)


# ##############################################################################
# CLI
# ##############################################################################


def main() -> None:
    """CLI entry point. Parse flags, dispatch ingest_corpus, print summary."""

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Ingest documents from the corpus into the RAG vector store.",
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=INGEST_DEFAULT_SAMPLE,
        help="Process only the first N documents (default: process all).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=INGEST_DEFAULT_DRY_RUN,
        help="Run the pipeline but skip the embed/store steps.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=INGEST_DEFAULT_DEBUG,
        help="Write per-stage outputs to debug/ingestion/ for inspection.",
    )
    parser.add_argument(
        "--corpus-dir",
        type=Path,
        default=Path(INGEST_CORPUS_DIR),
        help="Override the corpus directory.",
    )
    args = parser.parse_args()

    # Resolve debug directory based on the --debug flag
    debug_dir = Path(INGEST_DEBUG_DIR) if args.debug else None

    # Header for the run
    print(f"Ingesting from {args.corpus_dir}")
    if args.sample:
        print(f"  Sample:  first {args.sample} document(s)")
    if args.dry_run:
        print("  Dry run: embed and store steps skipped")
    if debug_dir:
        print(f"  Debug:   per-stage outputs to {debug_dir}/")
    print()

    # Run the orchestrator and print the summary
    report = ingest_corpus(
        corpus_dir=args.corpus_dir,
        sample=args.sample,
        dry_run=args.dry_run,
        debug_dir=debug_dir,
    )
    report.print_summary()
