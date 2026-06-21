# ##############################################################################
# File: ingest.py
# Purpose: Ingestion pipeline for the RAG knowledge base. Reads PDFs from
#          INGEST_CORPUS_DIR, runs them through parse -> QC -> (chunk -> embed
#          -> store), and isolates failures to a quarantine folder.
#
# Pipeline order:
#   parse_document -> quality_check -> chunk_document -> embed_chunks -> store
#
# Chunking, embedding, and storage are stubbed in Phase 1. The pipeline runs
# end-to-end, applies quality gates, and quarantines failures. Real chunking
# and embedding are wired in Phase 2 and Phase 3.
#
# Contents:
#   Classes:
#     Result                  - Outcome of processing one document
#     Report                  - Summary of a full ingestion run
#
#   Functions:
#     load_manifest()         - Read arxiv_id -> metadata mapping
#     parse_document()        - Parse a PDF via Docling (routing point reserved)
#     quality_check()         - Inspect parsed output for bad extraction
#     handle_failure()        - Move document to quarantine + write JSONL report
#     save_debug()            - Write per-stage output JSON for inspection
#     ingest_one()            - Process one document end to end
#     ingest_corpus()         - Loop over corpus, return Report
#     ingest_documents()      - Legacy wrapper for agent tool compatibility
#     main()                  - CLI entry point
# ##############################################################################


# Standard library
import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# Third-party
# Docling and langdetect imports are deferred to runtime inside the functions
# that need them, so the module can be imported without those packages being
# installed (e.g. when only the agent's search tool is being used).

# Local
from config import (
    INGEST_CORPUS_DIR,
    INGEST_DEBUG_DIR,
    INGEST_PROBLEM_DIR,
    INGEST_MANIFEST_PATH,
    INGEST_DEFAULT_SAMPLE,
    INGEST_DEFAULT_DRY_RUN,
    INGEST_DEFAULT_DEBUG,
    INGEST_QC_MIN_CHARS,
    INGEST_QC_MIN_ALNUM_RATIO,
    INGEST_QC_EXPECTED_LANGUAGE,
    INGEST_QC_STRUCTURE_MARKERS,
    INGEST_QC_MIN_ABSTRACT_OVERLAP,
)


# ##############################################################################
# Dataclasses
# ##############################################################################


@dataclass
class Result:
    """Outcome of processing one document.

    Attributes:
        doc_path (Path): The document this Result describes.
        status (str): One of "success", "failed", "exception".
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
    """Summary of a full ingestion run.

    Tracks per-document Results and produces a printable summary at the end.
    """

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
# Parsing
# ##############################################################################


def parse_document(path: Path) -> list:
    """Parse a single document into LangChain Document objects via Docling.

    Args:
        path (Path): Path to the PDF on disk.

    Approach:
        Currently always uses Docling via langchain-docling. This is the
        designated routing point for the future: when the system has to handle
        non-paper documents (forms, slides, scanned PDFs), replace the body of
        this function with a router that picks Docling, OCR pipeline, form
        parser, or slide parser based on document type. The signature stays
        stable so callers do not change. See DEVLOG section
        "Ingestion Design > Routing" for the design.

    Returns:
        list: LangChain Documents produced by DoclingLoader.
    """

    # Import inside the function so the module can be imported without docling
    from langchain_docling import DoclingLoader

    loader = DoclingLoader(file_path=str(path))
    return loader.load()


# ##############################################################################
# Quality check
# ##############################################################################


def quality_check(parsed_text: str, paper_meta: Optional[dict]) -> list[str]:
    """Inspect the parser output for signs of bad extraction.

    Args:
        parsed_text (str): The combined text content of the parsed document.
        paper_meta (Optional[dict]): The manifest entry for this paper, used
            for the abstract-overlap check. May be None or empty.

    Approach:
        Five cheap heuristics catch most silent parser failures: char-count
        floor, alphanumeric ratio, language detection (langdetect), expected
        paper structure markers, and abstract-overlap against the manifest's
        known abstract.

    Returns:
        list[str]: Failure reasons. Empty list means the document passed.
    """
    failures: list[str] = []

    # Empty or near-empty output
    char_count = len(parsed_text)
    if char_count < INGEST_QC_MIN_CHARS:
        failures.append(f"too_short ({char_count} chars)")
        return failures  # Other checks are meaningless on empty text

    # Alphanumeric / whitespace ratio (garbled output has low ratio)
    alnum = sum(c.isalnum() or c.isspace() for c in parsed_text)
    ratio = alnum / char_count
    if ratio < INGEST_QC_MIN_ALNUM_RATIO:
        failures.append(f"low_alnum_ratio ({ratio:.2f})")

    # Language detection (skipped if langdetect not installed)
    try:
        from langdetect import detect, DetectorFactory
        DetectorFactory.seed = 0
        lang = detect(parsed_text[:1000])
        if lang != INGEST_QC_EXPECTED_LANGUAGE:
            failures.append(f"unexpected_language ({lang})")
    except ImportError:
        pass
    except Exception:
        failures.append("language_detection_failed")

    # Expected structure markers for research papers
    text_lower = parsed_text.lower()
    has_markers = any(m in text_lower for m in INGEST_QC_STRUCTURE_MARKERS)
    if not has_markers:
        failures.append("no_paper_structure_markers")

    # Abstract overlap (corpus-specific: only runs if manifest has an abstract)
    if paper_meta and paper_meta.get("abstract"):
        abstract_words = set(re.findall(r"\w+", paper_meta["abstract"].lower()))
        text_words = set(re.findall(r"\w+", parsed_text.lower()))
        if len(abstract_words) > 0:
            overlap = len(abstract_words & text_words) / len(abstract_words)
            if overlap < INGEST_QC_MIN_ABSTRACT_OVERLAP:
                failures.append(f"abstract_overlap_low ({overlap:.2f})")

    return failures


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
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict") and callable(obj.dict):
        return obj.dict()
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    return str(obj)


# ##############################################################################
# Dedup and config hash
# ##############################################################################


def compute_config_hash() -> str:
    """Compute an 8-character hash of the ingestion-relevant config values.

    Approach:
        Hashes the JSON-serialized values that affect what chunks look like
        (embedding model, chunk size, chunk overlap, and any future values
        like chunking strategy or contextual prefix). When any of these
        change, the hash changes, which lets already_ingested() distinguish
        chunks ingested under one config from chunks ingested under another.

    Returns:
        str: First 8 hex chars of the SHA-256.
    """
    from config import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP

    payload = {
        "embedding_model": EMBEDDING_MODEL,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        # Phase 2 + 3 will add: chunking_strategy, contextual_prefix, parser, etc.
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()[:8]


def already_ingested(arxiv_id: str, config_hash: str) -> bool:
    """Check whether this document has chunks in the vector store under the current config.

    Args:
        arxiv_id (str): The document's arxiv identifier (filename stem).
        config_hash (str): The current run's config hash.

    Approach:
        Phase 3 will implement this by querying Chroma for chunks where
        metadata.arxiv_id == arxiv_id AND metadata.config_hash == config_hash.
        If any chunk matches, the document is already ingested under this exact
        config and should be skipped. Until storage is wired up, this returns
        False so every document gets processed.

    Returns:
        bool: True if already ingested under the current config, else False.
    """
    # TODO: Phase 3 - query the vector store for matching arxiv_id + config_hash.
    # Until then, the dedup hook is structurally present but never fires.
    _ = arxiv_id, config_hash  # both consumed in Phase 3; silence unused-param hints
    return False


# ##############################################################################
# Per-document orchestrator
# ##############################################################################


def ingest_one(
    doc_path: Path,
    manifest: dict,
    debug_dir: Optional[Path] = None,
    dry_run: bool = False,
) -> Result:
    """Process one document through parse -> QC -> chunk -> embed -> store.

    Args:
        doc_path (Path): The PDF to ingest.
        manifest (dict): The arxiv_id -> metadata mapping for joining intrinsic
            metadata onto each chunk.
        debug_dir (Optional[Path]): If set, per-stage outputs are written here.
        dry_run (bool): If True, the embed and store steps are skipped.

    Approach:
        Calls parse_document, gates with quality_check, then proceeds to the
        chunk and embed steps (currently stubs). On failure, returns a Result
        the orchestrator can hand to handle_failure.

    Returns:
        Result: Per-document outcome.
    """

    # Look up the per-paper intrinsic metadata
    arxiv_id = doc_path.stem  # "2606.20563.pdf" -> "2606.20563"
    paper_meta = manifest.get(arxiv_id, {})

    # Parse
    docs = parse_document(doc_path)
    if debug_dir:
        save_debug(debug_dir, arxiv_id, "parsed", docs)

    # Combine parsed text for QC (DoclingLoader may return multiple Documents)
    parsed_text = "\n\n".join(getattr(d, "page_content", "") for d in docs)

    # Quality check (gate before chunking)
    failures = quality_check(parsed_text, paper_meta)
    if failures:
        return Result.failure(doc_path, failures)

    # Chunking (stubbed in Phase 1)
    # When wired: chunks = chunk_document(docs, paper_meta)
    placeholder_chunk_count = max(1, len(parsed_text) // 1000)
    if debug_dir:
        save_debug(
            debug_dir,
            arxiv_id,
            "chunks_stub",
            {
                "note": "chunking not implemented in Phase 1",
                "parsed_text_length": len(parsed_text),
                "would_produce_roughly": placeholder_chunk_count,
            },
        )

    # Embedding + storage (stubbed in Phase 1)
    # When wired: vectors = embed_chunks(chunks); store(chunks, vectors, paper_meta)
    if not dry_run:
        # Phase 1: nothing is written to the vector DB yet.
        pass

    return Result.success(doc_path, n_chunks=placeholder_chunk_count)


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

    # Discover documents (non-recursive on purpose; legacy/ and problem/ stay out)
    docs = sorted(corpus_dir.glob("*.pdf"))
    if sample:
        docs = docs[:sample]

    # Ensure debug_dir exists if requested
    if debug_dir:
        debug_dir.mkdir(parents=True, exist_ok=True)

    report = Report(started_at=datetime.now(timezone.utc))

    # Process each document; orchestrator only orchestrates
    for doc in docs:
        arxiv_id = doc.stem

        # Dedup check: skip documents already ingested under current config.
        # Phase 1 stub always returns False, so this never fires until Phase 3.
        if already_ingested(arxiv_id, config_hash):
            result = Result.skipped(doc, f"already ingested under config {config_hash}")
            report.add(result)
            print(f"  {result.status:9s} {doc.name}")
            continue

        try:
            result = ingest_one(doc, manifest, debug_dir=debug_dir, dry_run=dry_run)
            report.add(result)
            if result.status == "failed":
                handle_failure(doc, result.failures)
        except Exception as e:
            result = Result.exception(doc, e)
            report.add(result)
            handle_failure(doc, result.failures)

        # Per-document progress line
        print(f"  {result.status:9s} {doc.name}")

    return report


# ##############################################################################
# Legacy wrapper for agent tool compatibility
# ##############################################################################


def ingest_documents() -> str:
    """Compatibility wrapper for the agent's ingest_documents_tool.

    Approach:
        Runs the new ingestion pipeline (parse + QC + stubbed chunk/embed)
        and returns a summary string the agent can read. In Phase 1 the
        chunking and embedding steps are stubs, so nothing is written to the
        vector store. Phase 3 wires those in.

    Returns:
        str: Summary string for the agent.
    """
    report = ingest_corpus()
    n_total = len(report.results)
    n_success = len(report.successes)
    n_failed = len(report.failures)
    return (
        f"Pipeline processed {n_total} document(s). "
        f"Parse+QC successful: {n_success}. "
        f"Quarantined: {n_failed}. "
        f"Note: chunking and embedding are Phase-1 stubs, "
        f"so no new chunks were added to the knowledge base."
    )


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
        print(f"  Dry run: embed and store steps skipped")
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


if __name__ == "__main__":
    main()
