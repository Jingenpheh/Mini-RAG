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
#     _load_dotenv_if_available() - Try to load .env, ignore failures
#     check_openai_key()          - Check OPENAI_API_KEY env var
#     check_config_importable()   - Check config.py loads
#     check_corpus_dir(path)      - Check corpus directory exists
#     check_chroma_dir(path)      - Check Chroma directory is creatable
#     check_package_imports()     - Check core mini_rag package imports
#     check_mcp_importable()      - Check MCP server module imports
#     check_vector_store()        - Check Chroma collection is reachable
#     check_setup()               - Orchestrate all checks, print, count
#     main()                      - CLI entry point
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


def _load_dotenv_if_available() -> None:
    """Best-effort .env load. Swallow errors so the check still reports cleanly."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass


def check_openai_key() -> tuple[bool, str]:
    """Confirm the OPENAI_API_KEY env var is set (loading .env as a fallback)."""
    if os.environ.get("OPENAI_API_KEY"):
        return True, ""
    _load_dotenv_if_available()
    if os.environ.get("OPENAI_API_KEY"):
        return True, ""
    return False, "set in env or in .env file at project root"


def check_config_importable() -> tuple[bool, str]:
    """Confirm config.py is importable without raising."""
    try:
        import importlib
        importlib.import_module("config")
        return True, ""
    except Exception as e:
        return False, str(e)


def check_corpus_dir(corpus_dir: str) -> tuple[bool, str]:
    """Confirm the configured corpus directory exists."""
    corpus = Path(corpus_dir)
    if corpus.exists() and corpus.is_dir():
        return True, ""
    return False, "create the folder or set INGEST_CORPUS_DIR env var"


def check_chroma_dir(chroma_dir: str) -> tuple[bool, str]:
    """Confirm the Chroma persist dir exists or can be created."""
    chroma = Path(chroma_dir)
    if chroma.exists() or chroma.parent.exists():
        return True, ""
    return False, "parent directory does not exist"


def check_package_imports() -> list[tuple[str, bool, str]]:
    """Confirm the three core mini_rag modules import. Returns one entry per module."""
    pkg_checks = [
        ("mini_rag.retriever", "from mini_rag.retriever import retrieve"),
        ("mini_rag.ingest", "from mini_rag.ingest import ingest_documents"),
        ("mini_rag.utils", "from mini_rag.utils import get_vector_store"),
    ]
    results: list[tuple[str, bool, str]] = []
    for label, import_stmt in pkg_checks:
        try:
            exec(import_stmt)
            results.append((label, True, ""))
        except Exception as e:
            results.append((label, False, str(e)))
    return results


def check_mcp_importable() -> tuple[bool, str]:
    """Confirm the MCP server module imports cleanly."""
    try:
        from mini_rag.mcp_server import mcp  # noqa: F401
        return True, ""
    except ImportError as e:
        return False, f"missing dep: {e}"


def check_vector_store() -> tuple[bool, int, str]:
    """Confirm the Chroma collection is reachable.

    Returns:
        (ok, count, detail). On success, count is the number of chunks in the
        collection. On error, count is -1 and detail carries the exception text.
    """
    try:
        from mini_rag.utils import get_vector_store
        store = get_vector_store()
        count = store._collection.count()
        detail = "run `python -m mini_rag.ingest --debug` if empty" if count == 0 else ""
        return True, count, detail
    except Exception as e:
        return False, -1, str(e)


def check_setup() -> int:
    """Run all deployment checks. Returns 0 if all pass, 1 if any fail."""

    failures = 0

    # OpenAI key
    ok, detail = check_openai_key()
    _check("OPENAI_API_KEY present", ok, detail)
    if not ok:
        failures += 1

    # Config import
    ok, detail = check_config_importable()
    _check("config.py importable", ok, detail)
    if not ok:
        # Can't continue without config
        return 1

    # Need config values for the path checks
    from config import INGEST_CORPUS_DIR, CHROMA_DIR

    ok, detail = check_corpus_dir(INGEST_CORPUS_DIR)
    _check(f"corpus dir exists ({INGEST_CORPUS_DIR})", ok, detail)
    if not ok:
        failures += 1

    ok, detail = check_chroma_dir(CHROMA_DIR)
    _check(f"Chroma dir creatable ({CHROMA_DIR})", ok, detail)
    if not ok:
        failures += 1

    # Package imports
    for label, ok, detail in check_package_imports():
        _check(f"import {label}", ok, detail)
        if not ok:
            failures += 1

    # MCP server import
    ok, detail = check_mcp_importable()
    _check("mini_rag.mcp_server importable", ok, detail)
    if not ok:
        failures += 1

    # Vector store reachable
    ok, count, detail = check_vector_store()
    label = f"Chroma collection reachable ({count} chunks)" if ok else "Chroma collection reachable"
    _check(label, ok, detail)
    if not ok:
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
