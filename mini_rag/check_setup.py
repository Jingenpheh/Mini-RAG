# ##############################################################################
# File: check_setup.py
# Purpose: Verify Mini-RAG's deployment configuration. Runs through a checklist
#          (env vars, paths, imports, vector store state) and reports green or
#          red per item. Useful for "I cloned this, why doesn't it work"
#          debugging.
#
# Run as:
#   python -m mini_rag.check_setup
#
# Contents:
#   Functions:
#     check_setup()             - Run all checks, print summary
#     main()                    - CLI entry point
# ##############################################################################


# Standard library
import os
import sys
from pathlib import Path

# Set up project root on path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def _check(label: str, ok: bool, detail: str = "") -> None:
    """Print one checklist line."""
    mark = "[ok]" if ok else "[!!]"
    line = f"{mark} {label}"
    if detail:
        line = f"{line} - {detail}"
    print(line)


def check_setup() -> int:
    """Run all deployment checks. Returns 0 if all pass, 1 if any fail."""

    failures = 0

    # Environment / API key
    has_key = bool(os.environ.get("OPENAI_API_KEY"))
    if not has_key:
        # Try loading from .env
        try:
            from dotenv import load_dotenv
            load_dotenv()
            has_key = bool(os.environ.get("OPENAI_API_KEY"))
        except Exception:
            pass
    _check(
        "OPENAI_API_KEY present",
        has_key,
        "" if has_key else "set in env or in .env file at project root",
    )
    if not has_key:
        failures += 1

    # Config import
    try:
        from config import (
            INGEST_CORPUS_DIR,
            CHROMA_DIR,
            EMBEDDING_MODEL,
            LLM_MODEL,
        )
        _check("config.py importable", True)
    except Exception as e:
        _check("config.py importable", False, str(e))
        failures += 1
        return failures  # can't continue without config

    # Corpus directory
    corpus = Path(INGEST_CORPUS_DIR)
    corpus_exists = corpus.exists() and corpus.is_dir()
    _check(
        f"corpus dir exists ({INGEST_CORPUS_DIR})",
        corpus_exists,
        "" if corpus_exists else "create the folder or set INGEST_CORPUS_DIR env var",
    )
    if not corpus_exists:
        failures += 1

    # Chroma directory or creatable
    chroma = Path(CHROMA_DIR)
    chroma_ok = chroma.exists() or chroma.parent.exists()
    _check(
        f"Chroma dir creatable ({CHROMA_DIR})",
        chroma_ok,
        "" if chroma_ok else "parent directory does not exist",
    )
    if not chroma_ok:
        failures += 1

    # Core package imports
    pkg_checks = [
        ("mini_rag.retriever", "from mini_rag.retriever import retrieve"),
        ("mini_rag.ingest", "from mini_rag.ingest import ingest_documents"),
        ("mini_rag.utils", "from mini_rag.utils import get_vector_store"),
    ]
    for label, import_stmt in pkg_checks:
        try:
            exec(import_stmt)
            _check(f"import {label}", True)
        except Exception as e:
            _check(f"import {label}", False, str(e))
            failures += 1

    # MCP server importable
    try:
        from mini_rag.mcp_server import mcp  # noqa: F401
        _check("mini_rag.mcp_server importable", True)
    except ImportError as e:
        _check("mini_rag.mcp_server importable", False, f"missing dep: {e}")
        failures += 1

    # Vector store reachable
    try:
        from mini_rag.utils import get_vector_store
        store = get_vector_store()
        count = store._collection.count()
        _check(
            f"Chroma collection reachable ({count} chunks)",
            True,
            "run `python -m mini_rag.ingest --debug` if empty" if count == 0 else "",
        )
    except Exception as e:
        _check("Chroma collection reachable", False, str(e))
        failures += 1

    print()
    if failures == 0:
        print("All checks passed.")
    else:
        print(f"{failures} check(s) failed. Fix and re-run.")
    return 1 if failures > 0 else 0


def main() -> None:
    code = check_setup()
    sys.exit(code)


if __name__ == "__main__":
    main()
