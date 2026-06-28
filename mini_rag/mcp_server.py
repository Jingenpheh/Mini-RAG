# ##############################################################################
# File: mcp_server.py
# Purpose: MCP server that exposes Mini-RAG to external agents. Provides four
#          tools (search, list, ingest, ingest-from-arxiv) and several
#          read-only resources (eval set, results, analysis docs).
#
# Pattern: this is the production interface to Mini-RAG. The dev agent at
# scripts/dev_agent.py is for local interactive testing; this MCP server is
# what consumer agents (Claude Desktop, Continue.dev, custom MCP clients)
# connect to.
#
# Run as:
#   python -m mini_rag.mcp_server
#
# Or wire into Claude Desktop via claude_desktop_config.json (see README).
#
# Contents:
#   Tools:
#     search_knowledge(query, k)     - Hybrid + reranked retrieval
#     list_corpus()                  - Inventory of ingested papers
#     ingest_new_documents()         - Scan corpus dir, ingest anything new
#     ingest_from_arxiv(arxiv_id)    - Download paper from arXiv + ingest
#
#   Resources:
#     eval://golden_set              - The 30-question golden eval set
#     eval://latest_results          - Latest eval run record (last line of
#                                       results.jsonl)
#     eval://baseline_analysis       - The v1->v5 journey analysis markdown
#     eval://v4_per_question_diagnosis - Per-question diagnosis at v4
#     corpus://manifest              - Inventory of ingested papers (JSON)
# ##############################################################################


# Standard library
import json
import ssl
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Set up project root on path so we can import the consolidated config
# and the package's sibling modules.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Third-party
import certifi  # noqa: E402
from mcp.server.fastmcp import FastMCP  # noqa: E402

# Local
from config import TOP_K, INGEST_CORPUS_DIR, INGEST_MANIFEST_PATH  # noqa: E402
from mini_rag.retriever import retrieve, list_sources  # noqa: E402
from mini_rag.ingest import ingest_documents  # noqa: E402


# ##############################################################################
# SSL trust store
# ##############################################################################

# urllib on Windows Python doesn't load a CA bundle by default, so the
# arxiv PDF download in ingest_from_arxiv fails with CERTIFICATE_VERIFY_FAILED.
# Point the default SSL context at certifi's bundle so urllib trusts the same
# CAs that requests does. Process-wide patch; fine for a single-purpose server.
ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)


# ##############################################################################
# MCP server instance
# ##############################################################################


mcp = FastMCP("mini-rag")


# ##############################################################################
# Tools
# ##############################################################################


@mcp.tool()
def search_knowledge(query: str, k: int = TOP_K) -> list[dict]:
    """Search the research-paper knowledge base.

    Runs hybrid (dense + BM25) retrieval followed by cross-encoder reranking
    over the indexed arXiv ML/AI papers. Returns the top-k most relevant
    chunks with their source metadata.

    Args:
        query: The search query in natural language.
        k: How many chunks to return (default: 5).

    Returns:
        List of chunks, each with:
          - chunk_id: e.g. "2606.20457::00042"
          - text: the chunk's content
          - arxiv_id: source paper's arXiv ID
          - title: source paper's title
          - section: section heading where the chunk lives
    """
    docs = retrieve(query, k=k)
    return [
        {
            "chunk_id": getattr(d, "id", None) or d.metadata.get("chunk_id", ""),
            "text": d.page_content,
            "arxiv_id": d.metadata.get("arxiv_id", ""),
            "title": d.metadata.get("title", ""),
            "section": d.metadata.get("section_heading", ""),
        }
        for d in docs
    ]


@mcp.tool()
def list_corpus() -> str:
    """List every paper currently ingested in the knowledge base.

    Returns:
        A human-readable summary with one line per paper showing the
        arXiv ID, title, and chunk count.
    """
    return list_sources()


@mcp.tool()
def ingest_new_documents() -> str:
    """Scan the corpus directory for new PDFs and process them.

    Reads INGEST_CORPUS_DIR (default ./docs/, env-overridable). For each
    PDF not already in the vector store under the current config hash,
    runs the parse -> QC -> chunk -> embed -> store pipeline. Skips
    documents already ingested (dedup via arxiv_id + config_hash).

    Returns:
        Summary string showing how many documents were processed,
        successful, skipped, and failed.
    """
    return ingest_documents()


@mcp.tool()
def ingest_from_arxiv(arxiv_id: str) -> str:
    """Download a paper from arXiv by ID and ingest it.

    Fetches the PDF, saves it to the corpus directory, then runs the
    ingest pipeline. Idempotent: if the paper is already ingested under
    the current config hash, it gets skipped by the dedup check.

    Args:
        arxiv_id: arXiv identifier, e.g. "2606.20457".

    Returns:
        Summary string describing what happened.
    """
    # Import arxiv inside the function so the module can be imported
    # without arxiv installed (it's in the sourcing dependency group).
    try:
        import arxiv
    except ImportError:
        return (
            "Error: arxiv package not installed. "
            "Run: uv sync --group sourcing"
        )

    # Resolve corpus dir
    corpus_dir = Path(INGEST_CORPUS_DIR)
    corpus_dir.mkdir(parents=True, exist_ok=True)

    # Check if PDF already on disk
    filename = f"{arxiv_id}.pdf"
    pdf_path = corpus_dir / filename
    already_on_disk = pdf_path.exists()

    if not already_on_disk:
        # Fetch from arXiv by ID
        client = arxiv.Client()
        search = arxiv.Search(id_list=[arxiv_id])
        try:
            result = next(client.results(search))
        except StopIteration:
            return f"Error: arXiv ID '{arxiv_id}' not found."
        except Exception as e:
            return f"Error fetching from arXiv: {e}"

        # Download the PDF
        try:
            urllib.request.urlretrieve(result.pdf_url, str(pdf_path))
        except Exception as e:
            return f"Error downloading PDF: {e}"

        # Update manifest with metadata so chunks get rich metadata at ingest
        manifest_path = Path(INGEST_MANIFEST_PATH)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest = {}
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except Exception:
                manifest = {}
        manifest[arxiv_id] = {
            "title": result.title.strip(),
            "authors": [str(a) for a in result.authors],
            "abstract": result.summary.strip(),
            "categories": result.categories,
            "primary_category": result.primary_category,
            "published": result.published.isoformat(),
            "updated": result.updated.isoformat(),
            "filename": filename,
        }
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    # Run the standard ingest pipeline; dedup handles re-runs cleanly
    summary = ingest_documents()
    prefix = "Already on disk; " if already_on_disk else f"Downloaded {arxiv_id}; "
    return prefix + summary


# ##############################################################################
# Resources
# ##############################################################################


_GOLDEN_SET_PATH = PROJECT_ROOT / "tests" / "eval" / "golden_set.jsonl"
_RESULTS_PATH = PROJECT_ROOT / "tests" / "eval" / "results.jsonl"
_ANALYSIS_DIR = PROJECT_ROOT / "tests" / "eval" / "analysis"


@mcp.resource("eval://golden_set")
def golden_set_resource() -> str:
    """The 30-question golden eval set as JSONL.

    Used by consumer agents to run their own end-to-end evaluation against
    the same questions Mini-RAG was internally evaluated against.
    """
    if not _GOLDEN_SET_PATH.exists():
        return ""
    return _GOLDEN_SET_PATH.read_text(encoding="utf-8")


@mcp.resource("eval://latest_results")
def latest_results_resource() -> str:
    """Latest internal eval run record as JSON.

    Reads the last line of tests/eval/results.jsonl. Useful for consumer
    agents that want to compare Mini-RAG's internal eval numbers against
    their own end-to-end eval numbers.
    """
    if not _RESULTS_PATH.exists():
        return "{}"
    last = ""
    with _RESULTS_PATH.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last = line.strip()
    return last or "{}"


@mcp.resource("eval://baseline_analysis")
def baseline_analysis_resource() -> str:
    """The v1 -> v5 cumulative journey analysis markdown.

    A reader-oriented narrative describing each iteration of Mini-RAG,
    the failures observed, the fixes applied, and the metric deltas.
    """
    path = _ANALYSIS_DIR / "baseline_analysis.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


@mcp.resource("eval://v4_per_question_diagnosis")
def v4_diagnosis_resource() -> str:
    """Per-question diagnosis at v4: status + remaining-fix analysis."""
    path = _ANALYSIS_DIR / "v4_per_question_diagnosis.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


@mcp.resource("corpus://manifest")
def corpus_manifest_resource() -> str:
    """The corpus manifest: arxiv_id -> metadata mapping for ingested papers."""
    path = Path(INGEST_MANIFEST_PATH)
    if not path.exists():
        return "{}"
    return path.read_text(encoding="utf-8")


# ##############################################################################
# Entry point
# ##############################################################################


def main() -> None:
    """Run the MCP server over stdio (the default transport for local MCP)."""
    mcp.run()


if __name__ == "__main__":
    main()
