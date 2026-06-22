# Mini-RAG Development Log

## Project Goal

Build a minimal RAG agent on OpenAI + LangChain + ChromaDB to get hands-on familiarity with the LangChain framework and explore RAG pain points in practice.

---

## Architecture & Project Structure

This project is small enough to fit in a single `main.py`. Even so, I followed standard structure: separate modules for configuration, tools, agent logic, and the entry point. The small upfront cost makes the project easier to read and extend later.

The tools folder splits ingestion and retrieval into independent files. They share one utility (`get_vector_store()` in `utils.py`) for connecting to Chroma, and beyond that they're decoupled. Keeping them independent meant I could write smoke tests for ingestion and retrieval on their own, before wiring them into the agent.

The agent has three tools: `search_knowledge`, `ingest_documents`, and `list_sources`. There's no fixed retrieve-then-generate pipeline. On each turn the agent decides which tool to call and when, reasoning about whether to search, ingest new documents, or just respond based on the conversation.

---

## RAG System

### Chunking

Chunking is the first decision in any RAG system. The options I looked at were fixed character splits, sentence and paragraph splits, recursive character splitting, and semantic chunking.

Semantic chunking is the strongest of these. It uses an embedding model to find meaning boundaries, so chunks line up with actual topic shifts. The cost is one embedding call per sliding window, which adds latency and API spend. For a small corpus of blog posts that cost isn't worth paying.

I went with **RecursiveCharacterTextSplitter** (500 characters, 100 character overlap). It tries paragraph breaks first, then sentence boundaries, then words, so chunks stay coherent without an embedding model. The 20% overlap means an idea that crosses a chunk boundary still appears in full in at least one chunk.

If retrieval quality becomes a problem later, the next thing to try is semantic chunking with a local embedding model, which avoids the per-window API cost.

### Corrective RAG

A common concern with RAG is that retrieved chunks might not actually answer the question. Similarity search returns text that's semantically close, which doesn't guarantee topical relevance. Some architectures handle this with an evaluation step between retrieval and generation, where an LLM checks whether the chunks are useful before the main agent answers.

I considered adding this, but the agent already handles it through the ReAct loop. When it receives search results, it reads them and decides whether they answer the question. If they don't, the system prompt tells it to rephrase the query and try again (up to 2 retries), then check for new documents to ingest. That's corrective RAG done through prompt engineering instead of as a separate evaluation chain.

Skipping the eval step keeps the system simple, with no extra LLM calls. The cost is less control. I'm relying on the agent's judgment instead of an explicit quality check, which is fine for this project. For a production system where accuracy matters more, an explicit eval step using something like RAGAS would be the better call.

### Document Parsing: Issues and Ideas

Document parsing turned out to be the messiest part of the project. Three issues came up.

Some PDFs saved from Chrome were image-based. PyPDFLoader returned zero characters because there was no text layer, only page screenshots. Re-saving the PDFs fixed it, but the lesson is that you can't assume a PDF has extractable text.

Even text-layer PDFs came out with messy formatting: one word per line, excessive spacing. A cleanup step (`re.sub(r"\s+", " ", text)`) before chunking collapses whitespace into readable text.

PDFs of web pages included navigation bars, footers, "Share on LinkedIn" buttons, and cookie banners. All of it gets chunked and embedded alongside the actual content. For a small corpus the noise is tolerable. At scale it would waste retrieval slots.

Taken together, these point at a deeper issue. A fixed parsing pipeline (always use PyPDF, always clean with regex) breaks the moment it sees a document it wasn't built for. Different documents need different strategies: text extraction for digital PDFs, OCR for scanned ones, structural parsing for tables and complex layouts.

One idea I had during this was a **document preprocessing agent**. It would sit before the embedding pipeline, inspect each incoming document, and route it to the appropriate parser. The agent would detect whether a PDF has a text layer or needs OCR, whether the content has boilerplate to strip, and whether tables need special handling. That turns preprocessing into an agentic step that adapts to whatever document comes in.

I didn't build this for the current project, but for a production RAG system it would be the natural next step.

---

## Agent Design

The agent uses the **ReAct** (Reasoning + Acting) pattern via LangChain's `create_tool_calling_agent`. Other patterns exist: Plan-and-Execute for long-horizon tasks with many sequential steps, Reflection / Self-RAG for self-correcting systems, multi-agent setups for complex multi-domain workflows. ReAct fits here because knowledge retrieval is a short-horizon task. The agent searches, looks at the results, decides whether more action is needed, then answers. No long-range planning required.

Something I want to record about how LangChain agents work under the hood: the LLM doesn't know it's inside a framework. On every API call, LangChain sends the tool definitions (name, description, parameter schema) alongside the conversation as a JSON payload. The LLM was trained to understand this format and respond with structured tool calls. This is why tool descriptions matter. The LLM reads them on every call to decide which tool to use and what arguments to pass.

### A note on MCP (Model Context Protocol)

During development I looked into whether MCP was relevant. MCP standardizes how tools are exposed and discovered across applications. Tools are registered once on an MCP server, and any MCP-compatible client can discover and call them.

For this project, the tools are defined in Python and used only by my own agent, so MCP adds no value. The picture changes in a larger setting. If a company has multiple teams building agents, and users running different interfaces (VS Code, Claude Code, Cursor, a custom web UI), every tool has to be re-implemented or wrapped per interface without MCP. With an MCP server, tools are defined once and shared across all of them.

MCP makes sense when you don't control all the interfaces that use your tools, or when tools need to be shared across teams. For a self-contained project where I define both the tools and the agent, LangChain's native tool system is enough.

---

## System Prompt Iteration Log

The system prompt went through three iterations. This is the part of the project I learned the most from.

**v1 (too loose):** The prompt said "don't hallucinate". When I asked about AMD gaming (not in the knowledge base), the agent searched, found nothing relevant, then answered with detailed information about Radeon RX and ray tracing pulled from its training data. There was no indication that the answer wasn't grounded in the knowledge base. That defeats the point of RAG. If the agent silently falls back to training data, you can't tell which parts of an answer are sourced.

**v2 (too strict):** I overcorrected to "NEVER generate information not returned by your tools". The agent refused everything. Even "hi there" got back "I don't have information about that in my knowledge base". It became a search terminal with no conversational ability.

**v3 (balanced, current):** The agent can converse normally and use general knowledge, but it has to clearly label what's from the knowledge base and what's not. AMD questions always search first. If the knowledge base doesn't have the answer, the agent can share general knowledge with a disclaimer attached. The aim is transparency. A good RAG assistant tells you what's sourced and what isn't, even when it's answering from general knowledge.

---

## Stack Choices

- **LLM: GPT-4o-mini.** Cheapest OpenAI model with solid tool-calling. Temperature=0 for deterministic, grounded answers.
- **Embeddings: text-embedding-3-small.** Already on the same OpenAI API key, so no additional provider needed. Higher quality than Chroma's default local model.
- **Vector store: ChromaDB.** Runs in-process with zero infrastructure (SQLite under the hood). Pinecone needs a cloud account, pgvector needs PostgreSQL, and FAISS has no metadata filtering. Chroma is the simplest option for a local project.
- **Framework: LangChain.** More flexible for agent orchestration than LlamaIndex, which is more opinionated about the RAG pipeline itself. This project is agent-first (retrieval is one tool among several), so LangChain's flexibility is the better fit.

---

## Testing Summary

**Ingestion.** 3 documents, 50 chunks. Deduplication verified (second run skips existing docs). Incremental ingestion works (only new PDFs processed). Empty chunk filtering and text cleaning verified.

**Retrieval.** Text accuracy is 100% against source documents. Relevance is around 75%. Some queries return tangentially related chunks. Embedding similarity captures semantic closeness, which doesn't always translate to topical precision. Re-ranking and query reformulation are the two improvements I'd reach for first to close that gap.

**Agent.** Searches before answering. Rephrases on insufficient results. Ingests when prompted. Handles casual conversation. Labels unsourced information with disclaimers. Cites documents and page numbers.

---

## Document Sourcing

The original AMD blog corpus did the job for the first version of the agent but it's the wrong shape for stress-testing real RAG. Five short blog posts mostly about one company won't surface ingestion or retrieval problems. To push the system further, I needed a bigger corpus made of harder documents.

I went with arXiv research papers in ML/AI categories. The choice felt simple and hard at the same time.

Simple, because arXiv has a public API and direct PDF URLs. No auth, no scraping, no fragile HTML, no rate-limit pain at moderate use. A script that pulls papers by category and date range and deduplicates against a local manifest covers the whole pipeline.

Hard, because research papers are exactly the kind of document that breaks naive RAG. They run 8 to 30 pages. Layout is non-standard: two-column text, figures with captions, dense tables of benchmark results, equations referenced inline from the prose. Naive text extraction loses most of the structure. Embeddings on flat token streams miss what matters most (figure context, table row meaning, equation references). This is exactly the corpus that will force me to engage with multimodal extraction, layout-aware parsing, and table handling rather than skip them as "future work".

### Fetcher

Built the fetcher at `scripts/sourcing/fetch_papers.py`. Default config pulls from `cs.AI`, `cs.LG`, `cs.CL`, `cs.CV`, `cs.IR`, `stat.ML`, up to 50 results per run, papers submitted in the last 30 days. First run brought down 50 papers from June 2026.

Deduplication is by canonical arXiv ID (stripping any version suffix like `v2`). A manifest at `scripts/sourcing/manifest.json` tracks what's been downloaded. Re-runs only pick up new papers.

The script uses `arxiv` 4.x. An earlier issue: `Result.download_pdf()` was removed in arxiv 4.0, so the script now downloads via `urllib.request.urlretrieve(result.pdf_url, ...)` directly. Works across older and newer versions of the library.

### Folder placement

First iteration put the script under `docs/sourcing/`, next to the data. That felt off after a few minutes of looking at it. `docs/` is supposed to be data the RAG reads. Mixing scripts in there blurs that role.

Moved to `scripts/sourcing/`. The rule I settled on:

- `docs/` is data the RAG reads
- `scripts/` is utilities the developer runs outside the RAG runtime
- `tools/` is what the agent calls during a session

Three folders, three clear roles. Future utility scripts (eval runners, migrations, etc.) can sit alongside `sourcing/` under `scripts/`.

### Dependency isolation

`arxiv` is a sourcing-only dependency. The RAG runtime doesn't need it. I put it in a `[dependency-groups.sourcing]` group in `pyproject.toml` so the main runtime stays lean. Anyone cloning the repo runs `uv sync --group sourcing` only if they want to fetch papers.

This also lines up with the longer-term plan: when an upstream agentic pipeline takes over and pushes documents in directly, the whole `scripts/sourcing/` folder and its dependency group can be deleted without touching anything in the RAG core.

### Git hygiene

PDFs are not tracked in git. Corpus is reproducible via the fetcher (or via the upstream pipeline later), and the PDFs are large. Added `docs/`, `.claude/`, and `scripts/sourcing/manifest.json` to `.gitignore`. The legacy AMD PDFs were also untracked at this point. They live in `docs/legacy/` for reference but won't be committed.

---

## Ingestion Design

Picking up from Document Sourcing. Once the corpus changed from AMD blog posts to arXiv research papers, the original ingestion pipeline stopped fitting. PyPDFLoader works for prose. It breaks on the multi-column layout, tables, figures, and equations that papers actually contain. Most of the design questions in this section came from "what do I do with these papers" rather than abstract architecture work.

### Metadata

My starting mental model was that metadata gets generated during embedding. That's wrong. Embedding only produces a vector. Metadata is everything else about a chunk: where it came from, when, what kind, what hierarchy it belongs to. It gets assembled separately and stored next to the vector in the same record.

A vector DB record looks like:

```
{
  id: "chunk_8432",
  vector: [0.034, -0.12, ...],
  text: "We observed a 40% reduction in P99 latency...",
  metadata: {
    arxiv_id: "2606.20563",
    title: "JanusMesh: Fast and Zero-Shot 3D Visual Illusion Generation...",
    primary_category: "cs.CV",
    published: "2026-06-18",
    page: 7,
    section: "Method",
    parent_chunk_id: "chunk_8430",
    ...
  }
}
```

The manifest at `scripts/sourcing/manifest.json` is the join table. When ingestion processes a paper, it loads the manifest entry by `arxiv_id` and attaches the intrinsic metadata (title, authors, abstract, categories, primary_category, published, updated, filename) to every chunk that paper produces. None of this requires an LLM call or anything clever. The information is already in the manifest from the sourcing step.

Reading around how teams structure metadata, the cleanest way to think about it is four sources, assembled at different points in the pipeline:

- **Intrinsic**: comes from the manifest. Free.
- **Parse-time**: extracted by the parser (page, section, region_type, bounding box).
- **Derived**: computed by code or small LLM calls (chunk_id, parent_chunk_id, char_count, document_summary).
- **Manual / external**: set by config or by the run itself (pipeline_commit, config_hash, ingested_at).

Some derived fields are worth the cost, some aren't.

**Document summary**: yes. One LLM call per paper, about $0.005 for the whole 50-paper corpus. Every chunk gets a doc-level summary attached, which gives the LLM something to anchor a retrieved chunk to during generation. Cheap and useful.

**Per-chunk enrichment** (chunk summaries, contextual chunking prefixes in the Anthropic style): skipping for now. The cost scales with the number of chunks, which is around three thousand on this corpus and millions at any enterprise scale. The retrieval-quality benefit is real but uncertain. With no eval set yet to measure whether it helps, the cost isn't worth paying.

**PII detection**: planning to wire up Microsoft Presidio. It's local, free, regex + spaCy NER based, no LLM calls. For the arXiv corpus there's nothing to detect, but for an enterprise version this matters and surfacing it in the pipeline is the right signal that I considered it. Important caveat: Presidio detects PII. It doesn't act on it. Whatever the system does with a detection (redact, restrict access, drop the chunk) is a separate decision and a separate piece of code I'd have to write.

**Pipeline versioning** (a manual/external field worth its own treatment): each chunk gets stamped with which version of the ingestion pipeline produced it, so later I can do things like "re-ingest anything older than version X" after I change chunking or parsing.

The obvious approach was a `pipeline_version = "v1.0"` constant that I bump manually whenever I change something meaningful. The problem with this is that manual bumping is the kind of discipline that works for the first month and then silently rots. People forget. Tiny changes don't get logged. The metadata starts lying.

Looking at how production teams handle this, the pattern is to drop the manual version entirely and use two auto-populated fields instead:

- `pipeline_commit`: the current git SHA, captured by running `git rev-parse --short HEAD` at ingestion start.
- `config_hash`: a SHA-256 of the JSON-serialized values of the ingestion-relevant config (embedding model, chunk size, overlap, parser choice, chunking strategy).

The git SHA tells me exactly what committed code ran. The config hash tells me what config it ran with, including uncommitted experimental changes. Together they tell me which chunks were produced under which conditions, with no human discipline required.

It's not a perfect substitute for a real semantic version. If I change something inside `ingest.py` without touching the config dict, the config hash won't move and only the git SHA will. Pattern coverage is roughly 80%. For a solo project that's enough. The point was to avoid metadata that I know will be unreliable.

### Parser choice

PyPDFLoader was right for the AMD blog corpus and wrong for research papers. Blogs are single-column prose. Papers are two-column with figures, tables, and equations. PyPDF strips all of that out and hands back word-soup that loses most of the document's structure.

Two parsers are realistic alternatives: Docling (IBM, free, runs locally) and LlamaParse (LlamaIndex, paid above a free tier, cloud API). On research papers specifically both produce good output. The decision came down to:

- Docling runs locally. No data leaves the machine, no API key, no recurring cost.
- LlamaParse premium edges ahead on the hardest documents (financial reports, slide decks with infographics), but the gap on papers is small.
- For a portfolio project the "I ran it locally" story is stronger than "I paid an API."

So Docling, via the `langchain-docling` package because it wraps Docling's output in LangChain's Document interface and makes it a near-drop-in replacement for `PyPDFLoader`. If later I want Docling's lower-level API for custom chunking or VLM-driven figure captioning, I can call docling directly.

LlamaParse stays in mind for two cases: (1) documents Docling visibly fails on, (2) a future demo where I want to show routing across multiple parsers.

### Routing

The routing question came up naturally from "Docling won't handle every document type." Real corporate inputs include scanned forms, slides, handwritten notes, CAD outputs, financial statements with footnote graphs. None of these route to "send to Docling and hope."

Reading around how production RAG systems handle this, the pattern is a routing layer that inspects the input and picks the right tool: file extension covers a lot (`.docx`, `.xlsx`, `.pptx`), a text-layer check distinguishes digital from scanned PDFs, folder structure helps, and for ambiguous cases you call a small classifier or VLM.

I'm not building any of that yet. The reasons:

- I have one document type. There's nothing to route to.
- Designing routing for documents I don't have is premature abstraction. I'd guess the wrong axes.
- The work distracts from things that matter more right now.

The compromise is a structural reservation. All ingestion calls go through one function `parse_document(path)` that currently just calls Docling. When routing becomes real, only that function changes. Everything calling it stays the same. The function carries a `TODO` comment so future me knows the design space was considered.

### Quality gates and error handling

Routing leads directly to: what happens if the parser is wrong for the document, or the right parser parses something subtly broken? Most parsers don't fail loudly. They return text regardless of whether the text is meaningful, and that gibberish gets chunked, embedded, and lands in the vector DB where it pollutes future queries.

The pattern teams use to catch this is quality gates: after the parser returns and before the chunker runs, a small function inspects the parsed output for signs of trouble:

- Character count below a threshold (extracted almost nothing).
- Low alphanumeric-to-total ratio (likely garbled).
- Language detection mismatch via `langdetect`.
- Missing structure markers a research paper should contain (Abstract, Introduction, Conclusion, References).
- Abstract-overlap check: compare the words in the manifest's known abstract to the extracted text. If the overlap is too low, the parser didn't pull the paper meaningfully.

If any of these fail, the document is treated as failed. It doesn't get chunked, doesn't get embedded, doesn't reach the vector DB. Instead it moves into a quarantine folder at `debug/ingestion/problem_documents/`, alongside a JSONL report with the same base name (`<arxiv_id>_failure_report.jsonl`) listing the failure reasons. Opening the folder, you see the PDF and its diagnosis side by side. No grep through a master log.

If someone inspects a problem document and decides it was a false alarm (or fixes the underlying issue), they move the PDF back into `docs/` and the next ingestion run picks it up. Fully reversible.

The principle is loud failure preferred over silent pollution. Better to skip a document and surface it for review than to let bad content silently degrade the retrieval quality of the whole index.

### Chunking

The first version of this project used `RecursiveCharacterTextSplitter` at 500 characters with 100 overlap. That was the right call for the AMD blog corpus where the documents were single-column prose. On research papers it isn't. Papers are arranged in sections and paragraphs by the author, and that structure carries semantic meaning the splitter can't see. Cutting at character count drops you mid-thought half the time, and a chunk that starts at "...this loss function performs" and ends with "...we trained for 100 epochs" lumps two different topics into one muddy embedding.

I looked at five alternatives:

**Semantic chunking.** An embedding model finds boundaries by detecting similarity drops between adjacent sentences. The theoretically clean answer. The cost is embedding every sentence to find the breaks, and the benefit assumes the document has no existing semantic structure to lean on. For research papers the author already imposed semantic boundaries through sections and paragraphs, so this is doing the work twice. It earns its complexity on unstructured text (scraped pages, transcripts, contracts), not on papers.

**Hierarchical chunking with parent-document retrieval.** Embed small leaf chunks (sentences) for precision, return parent chunks (sections) to the LLM for context. The pattern has real benefits in production but doubles storage and adds a parent lookup step on every retrieval. With no eval set yet to prove the gain, the cost isn't worth paying. The schema I went with is forward-compatible so this can be added later without re-ingest if the eval shows we need it.

**LLM-as-chunker.** Pass the document to an LLM and ask it to mark chunk boundaries. The copy-paste failure mode is real (LLMs paraphrase, drop content, mangle special characters), the cost scales linearly with corpus size, and there's no eval evidence the gain justifies it. The boundary-only variant (LLM outputs sentence indices for breaks, never reproducing the text) avoids the copy-paste hazard but still costs per document and isn't justified without baseline numbers.

**Docling's HierarchicalChunker.** What `langchain-docling`'s `DoclingLoader` returns by default. Groups `doc_items` by section under a size budget. Inconsistent in practice: sometimes it groups title + author + affiliation into one front matter chunk (good), sometimes it groups multiple body paragraphs into one super-chunk (muddy). The grouping isn't documented as deterministic.

**Paragraph-level chunking from docling's `DocumentConverter` directly.** What I went with. Skip the HierarchicalChunker and iterate docling's raw `doc_items`. The reasoning: docling's layout model identifies text blocks at the paragraph level. For body content, one `doc_item` is one paragraph. For special structures, one doc_item is one list_item, one formula, one table, one caption. This gives chunking semantics that don't depend on a heuristic grouper.

The implementation iterates doc_items in document order, one chunk per doc_item, with two refinements:

- **Small-item merge.** Consecutive same-section same-label doc_items under 200 characters get merged into a single chunk. This re-creates the good HierarchicalChunker behavior for front matter (title, author, affiliation coalesce) without re-grouping full body paragraphs.
- **Size safety net.** Chunks under 30 characters get dropped (page numbers, stray artifacts, single-character page headers). Chunks over 2000 characters get split on sentence boundaries.

Section context is preserved by walking the doc_item's parent reference up to the nearest section heading and attaching it as the chunk's `section_heading` metadata.

These choices are calibrated for research papers. Slides, code, contracts, and forms would all need different chunking strategies. The routing branch I left in `parse_document` extends naturally to chunking when those document types arrive. For now there's nothing to route.

### Artifacts: formulas, tables, figures

A research paper isn't just prose. Equations, tables, and figures carry real information and degrade in different ways through PDF parsing.

**Formulas.** Docling's default returns `<!-- formula-not-decoded -->` as a placeholder. Enabling structured formula extraction makes docling attempt LaTeX output. Some papers work, some don't. The cases where it fails: equations rendered as images even in digital PDFs (some LaTeX-to-PDF pipelines do this), complex multi-line equations, custom symbol libraries.

The plan: try extraction. On success, attach the LaTeX to the preceding text chunk, which is the chunk that introduces the equation ("...we define forward diffusion by means of the SDE:"). The embedding reflects the explanation; the LLM sees the formula alongside the explanation when the chunk gets retrieved. On failure (placeholder detected by string match), drop the formula. The preceding text still describes its purpose, so the retrieval signal is preserved.

Why preceding rather than following: the text leading into an equation usually names it ("we define X by the SDE"), which is what a query like "what SDE does the paper use" matches against. The text following an equation typically defines variables ("where X_0 is..."), which works as its own searchable chunk without needing the equation embedded.

**Tables.** Default docling output flattens tables into noisy "key. = value" strings, one per cell, with the 2D relationship lost. Useless for retrieval and bad for an LLM trying to reason about results.

Better: enable docling's structured table extraction, format the result as a markdown table, embed the markdown along with its caption. Markdown preserves the row and column relationships as text, which LLMs handle reasonably well for the small table sizes typical in papers (4-6 columns, under 20 rows). For larger tables the markdown approach degrades; the fallback would be storing tables as separate structured records rather than embedding their text, which is a phase-later decision if the eval shows it matters.

**Figures.** Docling doesn't extract figures by default. Even with extraction enabled, the result is a bounding-box reference, not searchable content. Real figure understanding requires a vision-language model to caption them, which costs roughly $0.001 per figure with gpt-4o-mini vision.

For now, I'm relying on captions. Captions describe what the figure shows ("Figure 3: loss curves for the three baselines"), are independently informative, and are already in the parsed output as `caption` doc_items. A query about figure content matches the caption; an answer cites the paper and page number for the reader to inspect the actual figure. Adding VLM captioning is the upgrade path if the eval surfaces figure-content queries that captions can't answer.

### Pipeline order

Parse → QC → PII → chunk → embed → store. QC sits between parsing and chunking so the pipeline bails out before doing chunking work on garbage. PII scrubbing sits between QC and chunking so that any redaction happens before content gets split into chunks (otherwise the same PII might leak across chunk boundaries). PII is currently a passthrough stub; the slot exists so the call site is in the right place when Presidio gets wired up. There's a small chunk-level QC pass possible after chunking (catch empty chunks, etc.) but it's cleanup, not the main gate.

### Checkpointing and inspection

For inspection during development, the ingestion orchestrator takes three flags:

- `sample`: process only the first N documents.
- `dry_run`: skip writing to the vector DB.
- `debug_dir`: when set, write per-stage outputs as JSON for inspection.

Running with all three on a single paper shows exactly what each stage produced. Running with none of them is production mode. This gives me the factory-floor inspection window without leaving artifacts in production runs.

All inspection output lands in `debug/`, which is gitignored. Per-stage subfolders (`debug/ingestion/`, eventually `debug/chunking/` and so on) keep different stages separated as the project grows. The discipline is "debug outputs are throwaway, written only when explicitly requested." Periodic cleanup is a one-liner:

```bash
find debug/ -maxdepth 1 -mindepth 1 -mtime +7 -exec rm -rf {} +
```

Manual chore or wired to a pre-commit hook later.

---

## Future Improvements

**Semantic chunking.** Use a local embedding model to find meaning boundaries instead of character boundaries, which avoids per-window API cost.

**Document preprocessing agent.** An agent sitting before the embedding pipeline that inspects each document and routes it to the right parser (text extraction, OCR, or structural parsing), replacing the fixed pipeline.

**Re-ranking.** After initial retrieval, rescore results with a cross-encoder model to filter out chunks that are semantically close but topically off.

**Query reformulation.** Generate multiple query variants per search using LangChain's `MultiQueryRetriever`, then merge and deduplicate results.

**Evaluation framework.** Automated retrieval and answer evaluation using RAGAS or LangChain's eval tools. Key metrics are faithfulness (answer matches sources), relevance (chunks match query), and completeness (all aspects addressed). Agent tool usage patterns are also worth tracking, to check whether the agent is choosing the right tool for each situation.
