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

### Embedding model

Three categories to choose from: hosted API (OpenAI, Cohere, Voyage), local general-purpose (BGE, E5, mxbai), local domain-specialized (SPECTER2, SciNCL).

OpenAI's `text-embedding-3-small` is the consistent-stack default. The LLM is already OpenAI, so adding the embedding API is one less moving piece. Cheap (around $0.02 per million tokens), reliable, easy to swap. The downside: generic, not tuned for academic papers, fixed at 1536 dimensions.

SPECTER2 (Allen AI) is trained specifically on academic literature. It's 768-dim, runs locally via `sentence-transformers`, no per-token cost, and outperforms general models on academic retrieval benchmarks. Setup cost is one extra dependency (`langchain-huggingface` + `sentence-transformers`) and a one-time model download (~400 MB) into the Hugging Face cache.

I went with SPECTER2. The reasoning:

- The corpus is academic papers. A domain-specialized model is the obvious fit.
- The cost difference is real but small. OpenAI is about $0.03 to embed 50 papers in ~30 seconds. SPECTER2 is free but takes ~3 to 5 minutes on CPU.
- The portfolio story is better. "Picked SPECTER2 because it's trained on papers" reads as deliberate. "Used OpenAI" reads as default-tier.
- The operational cost is one extra dependency, not a meaningful burden for this project.

I deliberately skipped the A/B comparison between SPECTER2 and OpenAI for now. Without an eval set there's no way to attach numbers to the choice, and running both models is the kind of work whose value lands once measurement exists. The trigger to revisit: if Recall@5 on the eval set comes in low after retrieval tuning is exhausted, comparing embedding models becomes the next lever.

The embedder lives behind a shared singleton in `tools/utils.py` so the model loads once per process and is reused by both the ingestion pipeline (embedding chunks) and the retriever (embedding user queries). Lazy init keeps `python -m tools.ingest --help` fast.

A subtle consequence of switching models: vector dimensions are baked into the Chroma collection at creation time. SPECTER2 at 768 dims is incompatible with OpenAI 3-small at 1536. Swapping models means wiping the collection and re-ingesting. The `config_hash` already covers this, so chunks ingested under one model get tagged differently than chunks under another, and dedup would not silently cross models.

### Vector database

The shortlist: Chroma (current), pgvector (Postgres extension), Qdrant (standalone Rust server), Weaviate (standalone, feature-rich), Pinecone (managed cloud), LanceDB (embedded).

I kept Chroma. The reasoning:

- Corpus scale is small. 50 papers × ~60 chunks ≈ 3000 vectors. Every candidate handles this comfortably.
- Setup cost difference matters. Chroma is `pip install` with data in `./chroma_db/`. pgvector needs a running Postgres container. Qdrant needs a running binary. Pinecone needs an account, an API key, and ongoing cost.
- Without an eval set, comparing vector DB performance is guessing. The choice between Chroma and (say) Qdrant should be made with numbers, not speculation.
- The storage layer in this pipeline is one function in one file (`tools/ingest/storage.py`). Swapping backends is an afternoon's work whenever it becomes necessary, and the rest of the code does not care which backend it is hitting.

The trigger to revisit: when the eval set is wired and I want to compare retrieval strategies, Chroma's hybrid search story (BM25 + dense) is the weakest among the candidates. At that point the move would be pgvector (the boring infrastructure choice, SQL filters, hybrid via tsvector) or Qdrant (the best pure-vector experience, native hybrid).

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

## Retrieval Design

The first version of retrieval used Chroma's `similarity_search` directly: embed the query with the same model used at ingestion (SPECTER2), take top-k by cosine similarity, return the Documents. Pure dense, no fusion, no reranking. That's the baseline this section iterates on.

### Why hybrid retrieval

The eval baseline (see the Evaluation section below) showed pure dense at Recall@5 = 0.103. The per-type breakdown was the diagnostic: definition and contribution_recall worked, but specific_fact_lookup, methodology, equation, and table_numerical all bottomed out near zero.

The pattern across the failures was the same. SPECTER2 was trained for paper-to-paper similarity. It maps "what dataset is introduced by SARLO-80" into a fuzzy cloud of dataset-related content across the entire corpus. The chunk that actually answers the question contains the specific terms ("Umbra Collection", "SICD scenes", "2,565") but doesn't repeat the paper's own name. The embedding can't bridge the gap from the question's anchor ("SARLO-80") to the answer chunk's content terms.

Reading around how production RAG systems handle this, the standard fix is hybrid retrieval: run a keyword retriever in parallel with the dense one and fuse their rankings. The keyword retriever (BM25) does what dense can't do: exact-term matching on acronyms, numbers, proper nouns, technical jargon. Dense does what BM25 can't: semantic paraphrase, conceptual matching, synonyms. Combined via Reciprocal Rank Fusion, each catches what the other misses.

### BM25 + dense via RRF

BM25 (Best Match 25) is the standard probabilistic keyword retrieval function from the 1990s. The "25" is just the experimental iteration number from Robertson and Spärck Jones's series at City University London; nothing significant. The math weighs term frequency in a document, inverse document frequency across the corpus, and document length normalization. Practically: documents containing the query's rare terms score high, documents that just have generic words don't.

For fusion, RRF was the right call over weighted score combination. Each retriever produces a ranked list. For each chunk that appears in either list, the RRF score is `sum of 1/(K + rank)` across both lists, with K = 60 as the standard constant. Chunks ranked at the top of both lists score highest, but chunks ranked top in only one still get a score and compete for the final top-k. The fusion doesn't try to compare BM25's term-overlap scores against dense's cosine scores directly; it just compares ranks, which is robust across very different scoring scales.

### Implementation: in-memory, no separate index database

The BM25 "index" is just tokenized text + term-frequency statistics. For 7,631 chunks it's roughly 50 MB of RAM and rebuilds in about a second from chunks already in Chroma. I considered three options:

- **External index (ElasticSearch, OpenSearch, Postgres tsvector)**: heavy infrastructure for the scale, no benefit.
- **Pickled on disk between runs**: small startup speedup (~1 second saved) at the cost of cache-invalidation complexity. Not worth it.
- **In-memory, rebuild at process startup, lazy singleton**: simplest, matches the existing pattern for the SPECTER2 embedder singleton.

I went with the in-memory singleton. The BM25 index lives in `tools/retriever.py` next to the `retrieve()` function that uses it. I deliberately did not put it in `tools/utils.py` even though that file holds the embedder and vector-store singletons. The rule for `utils.py` is "things both ingestion and retrieval need to share"; BM25 is only used at query time, so it belongs in the retrieval module.

The `retrieve()` function is the single entry point. Both `search_knowledge()` (the agent tool) and the eval script call it. Hybrid behavior gets inherited by every retrieval surface automatically.

### What hybrid still can't do

The eval surfaced three categories where hybrid retrieval moved the needle from zero to zero. These aren't BM25 or dense failures; they're properties of single-pass retrieval that no amount of retriever tuning can fix:

- **Multi-hop questions** ("Which related-work item discusses lottery, and what does it say"): require finding A, then formulating a follow-up query about A, then returning B. Single-pass retrieval has no decomposition step.
- **Cross-paper questions** ("How do JanusMesh and Thinking in Boxes differ"): require fetching content from two distant papers and synthesizing. A single embedding cannot equally serve two unrelated topics.
- **Vague-ambiguous questions** ("Tell me about image editing"): the query has no anchor for the system to grip onto. A real consumer would ask for clarification; raw retrieval has no clarification mechanism.

These belong in the agent layer that consumes this RAG, not in the RAG itself. Their zero scores in the eval are evidence of where the boundary lies, not failures to fix.

### What's left at the retrieval layer

Cross-encoder reranking is the obvious v3 candidate. Hybrid retrieval got us into the right region but not always to the right chunk: for `table_numerical` questions, retrieval pulls the table caption and surrounding analysis but misses the specific row chunk holding the exact number. A reranker rescores the top-20 RRF results with a model trained for query-passage relevance directly, pushing the precise chunk above the noisy adjacent ones. The fix for `table_numerical` Recall@5 = 0 lives here.

Table-specific chunking is the other thread. The current chunker splits tables into row-level chunks via Docling's structured output, which works for big tables and breaks for queries about specific rows. Keeping each table as one chunk (caption + all rows joined) is a defensible alternative; I haven't implemented it because it conflicts with the size ceiling on the rest of the chunker.

Both belong on the v3 roadmap. Sequencing depends on which gap the next iteration prioritizes.

---

## Evaluation

The eval set is the highest-leverage thing in the project. Without it, every change after this point reads as opinion. With it, every change has a number attached. This section captures what I built, what I learned about question design, and what the v1 → v1.1 → v2 numbers actually say.

### Why evaluate at all (and why before the MCP wrapper)

CLAUDE.md's re-scoped priorities put the eval set second, just after the validation experiment. The reasoning held up: I learned more from running the v1 baseline than from any single architectural decision in this project so far. The baseline numbers told me exactly which categories the system handled and which it failed on, which directly drove the v1.1 chunker fix and the v2 hybrid retrieval upgrade. Without those numbers, I would have been guessing about which improvement to pursue first.

The other reason I did this before MCP is that the eval defines what "the RAG" is. The eval set is the contract: these are the questions the system is supposed to answer well. Once that's stable, the MCP tool surface that exposes the RAG to external agents has a measurable definition behind it. Building MCP first and then evaluating would be backwards.

### Two layers of metrics

I went with both custom retrieval metrics and RAGAS. The split:

- **Custom (Recall@1, Recall@3, Recall@5, MRR, NDCG@5)**: deterministic, no LLM cost, computed from chunk_id matching against the golden set. Tells me whether the right chunk was retrieved. Pure retrieval signal.
- **RAGAS (faithfulness, context_precision, context_recall, answer_correctness, answer_relevancy)**: LLM-judged on top of a minimal generation step. Tells me whether the retrieved chunks were USEFUL beyond the chunk_id strict-match.

The reason for both: context_precision in particular saved me from misreading the methodology results. The v1 baseline showed methodology Recall@5 = 0 but context_precision = 0.904. That gap meant the retriever was finding RELEVANT content from the right paper, just not the specific chunk I had marked as gold. The chunk_id strict-match metric was overly punishing; the LLM-judge metric saw through to "this is methodology content from the right paper". Without RAGAS I would have over-corrected by widening the gold_chunk_ids; with RAGAS I could leave them and let context_precision carry that signal.

For the eval-time generation step that RAGAS needs an answer for, I deliberately keep the LLM call minimal. No agent loop, no tool use, no fancy prompting. Just "given these chunks, answer this question". That's a floor on what any reasonable consumer of the RAG could do. If the minimal generator can produce a faithful, correct answer, anything more sophisticated will at least match it.

### Question typology

I built the golden set around a typology of question categories rather than just picking 30 questions ad-hoc. Each category tests a different property of the system. The 11 types I ended up using:

- **specific_fact_lookup** (6 questions): a precise fact appearing in a single chunk. Tests dense embedding precision plus exact-term match.
- **definition** (4): "what is X" where X is a paper-specific term. Tests whether the semantic embedding maps the term to its definition chunk.
- **methodology** (4): "how did they do Y". Tests section-level retrieval of the methods section.
- **table_numerical** (3): a specific value from a table. Tests how tables come through chunking and whether the value is retrievable.
- **equation** (2): a specific formula. Tests whether equations land in chunks at all (they did not until the chunker fix), and whether dense retrieval can find math content.
- **comparison_contrast** (3): two things compared within one paper. Tests multi-section synthesis.
- **contribution_recall** (3): "what are the contributions". Tests list-item retrieval.
- **cross_paper** (2): compare two different papers. Tests multi-document retrieval. Predicted to fail at the RAG layer.
- **negative_no_answer** (1): a question the paper doesn't answer. Tests grounding: does the system refuse to hallucinate?
- **vague_ambiguous** (1): "tell me about X" with no anchor. Tests query-understanding boundary. Predicted to fail at the RAG layer.
- **multi_hop** (1): "find the thing about X and tell me what it says". Tests decomposition. Predicted to fail at the RAG layer.

Three of the categories (cross_paper, multi_hop, vague_ambiguous) I included DELIBERATELY KNOWING they would score zero at the RAG layer. Their value is documenting where the agent-layer boundary lies. When the eval shows them at zero across v1, v1.1, and v2, that's evidence I can point at in the writeup: these aren't RAG failures, they're scope decisions.

### What I got wrong about question crafting

The first draft of the golden set had questions like "What dataset did this paper use?" and "What evaluation metrics did the team use in this paper?". I had written them while looking at specific papers, and the paper context was implicit in my head. When the eval ran, Recall@5 came back near zero across these questions even though the answers were trivially in the corpus.

The reason was that the retriever has no implicit paper context. "This paper" is meaningless to a system processing a standalone query. SPECTER2 mapped "What dataset did this paper use" to a fuzzy cloud of dataset-related content across all 50 papers; it picked chunks discussing the COMPAS dataset, public dataset comparisons, and licensing tables from totally unrelated papers, all of which contained the word "dataset" but none of which were the gold paper.

The lesson: a question that doesn't disambiguate itself can't be answered by retrieval alone, no matter how good retrieval is. In real consumer use, the question carries context: the user typed it because they were reading the paper, and the surrounding context provides the disambiguation. In standalone eval, the question has to carry the disambiguation itself.

I rewrote 14 of the 30 questions to include the paper's distinctive name or technical anchor:

- "What dataset did this paper use?" → "What dataset is introduced by SARLO-80?"
- "What evaluation metrics did the team use in this paper?" → "What evaluation metrics does CalTennis use for monocular-to-3D tennis pose estimation?"
- "What is the third takeaway of the experiment in this paper?" → "In the Calibrated Mixture-of-Experts under Distribution Shift paper, what is the third takeaway from the experiments?"

The anchor doesn't have to be the full paper title. The most effective rewrites used the paper's distinctive proper noun: a system name (SARLO-80, CalTennis, MAA, ACE, JanusMesh), a method name, or a technical phrase that appears in the chunk content. arxiv_ids don't help because the ID isn't in the chunk text; SPECTER2 never sees the digit string in a context that would help it match.

### What the v1, v1.1, v2 numbers said

I tracked three versions, each isolating one change:

- **v1**: pure dense retrieval, current chunker. Baseline.
- **v1.1**: chunker fix (Docling `FormulaItem.orig` fallback). Recovers formula content that v1 silently dropped.
- **v2**: hybrid retrieval (BM25 + dense via RRF).

The progression of overall Recall@5: 0.103 → 0.103 → 0.276. v1.1 didn't move retrieval rank metrics because the formula CONTENT landing in chunks doesn't help if the chunks aren't being ranked higher. But v1.1 did move RAGAS context_recall up by +0.034 because the retrieved chunks now contained more of the gold answer text. The fix was necessary scaffolding; v2 unlocked its value.

v2 (hybrid) is where the numbers actually moved. Recall@5 nearly tripled, every RAGAS metric jumped, and the equation type went from 0.000 to 0.500 (the combined v1.1 + v2 win). Categories that needed the agent layer (cross_paper, multi_hop, vague_ambiguous) stayed at zero across all three versions, as predicted.

The full per-version comparison lives at `tests/eval/analysis/baseline_analysis.md`. The structure is: headline numbers, per-type breakdown, findings, per-question highlights, run metadata. Three sections, one per version, so a reader can see the deltas at a glance.

### Reproducibility: the corpus lock file

The eval is only useful if someone else can run it. The arxiv papers in `docs/` are gitignored (250 MB), the manifest is gitignored too (per-developer dedup state), and the original `fetch_papers.py` pulls papers by category + date, which is non-deterministic by design.

The fix is a small JSON lock file at `scripts/sourcing/eval_corpus.json` listing the exact 50 arxiv_ids the eval set is built against. A new function `fetch_eval_corpus()` in `fetch_papers.py` queries arxiv by exact id_list (deterministic) and downloads those papers. A fresh clone can reproduce the eval environment with one command. The repo stays small (no PDFs), and the eval still has the realistic 50-paper distractor corpus that makes retrieval testing meaningful.

### What I'd add to the eval set later

Categories worth adding once the system can handle them:

- **Cross-section synthesis within a single paper**: queries that explicitly require combining content from the methods and results sections. Tests reranking and parent-doc expansion together.
- **Negative-cross-paper**: "Does paper X discuss Y" where X exists but Y is not in X. Tests grounding across the multi-doc surface.
- **Date-sensitive**: "What is the most recent paper in the corpus that mentions Z". Tests metadata filtering.
- **Adversarial paraphrase**: same factual question asked with completely different vocabulary. Tests embedding robustness directly.

I haven't added these yet because each requires either an agent layer (cross-section), a multi-doc retrieval pattern (negative-cross-paper), or features I haven't built (metadata range queries). They're queued for after the next architectural step.

---

## Cross-encoder Reranking (v3)

v2's hybrid retrieval got Recall@5 from 0.103 to 0.276. The per-question audit (`tests/eval/analysis/v2_per_question_diagnosis.md`) showed two distinct failure modes left:

1. The right chunk was in the top-20 but ranked between 6 and 20. Reranking would solve this.
2. The right chunk was past rank 100 in both BM25 and dense (Q01 SARLO-80 at rank 200+, Q07 MAA at rank 1868). No reranker can recover what was never retrieved.

I added a cross-encoder reranking stage to fix category 1. The flow becomes: dense top-20 plus BM25 top-20 fused by RRF, then the top-N of the fused pool rescored by a cross-encoder, then top-k returned to the caller.

### Model choice

`cross-encoder/ms-marco-MiniLM-L-6-v2` from sentence-transformers. 80 MB, MS-MARCO trained, runs on CPU in under a second per query for a pool of 50. It's the standard small cross-encoder; I chose it for the local-CPU constraint and the fact that MS-MARCO is the right training domain (text passage relevance). A SciFact-trained or table-specialized model would be the next thing to try, but at this corpus size the difference doesn't show up cleanly on the eval set.

The reranker singleton lives in `mini_rag/retriever.py` rather than `mini_rag/utils.py`. `utils.py` holds resources shared between ingest and retrieve (embedder, vector store, BM25 corpus loader). The cross-encoder is only used at retrieve time, so it stays with the retriever.

### What the v3 numbers said

Overall Recall@5: 0.276 → 0.310. The lift was real but smaller than the v2 jump. The reranker recovered cases where the gold chunk was in the fused top-20 but ranked below noise. It didn't touch the deep failures (Q01, Q07 still at zero) because the chunks weren't in the candidate pool. That confirmed the diagnosis: the next fix had to be at the candidate-generation layer, not the rescoring layer.

The reranker also held context_recall flat and lifted faithfulness slightly. It's doing what it should: changing which top-5 chunks the LLM sees, not what's in the pool.

---

## Contextual Chunking (v4)

The v3 audit confirmed the rank-200+ failures came from a structural mismatch. Q01 asked about SARLO-80, the paper's named system. The chunk holding the answer didn't say "SARLO-80" anywhere; the paper introduced the name on page 1 and used "our system" thereafter. SPECTER2 embedded the chunk as generic methods text. BM25 had no token to match. Both retrievers missed.

The fix: prepend a contextual prefix to every chunk before embedding and BM25 indexing. The prefix is `"Paper: <title>\nSection: <section>\n\n"` followed by the original chunk text. Every chunk now carries the paper's title and the section heading inside its searchable text.

### Why inline prefix and not a separate field

I considered putting the title and section in a separate metadata field and indexing it independently with weight. I went with inline prefix because:

1. BM25 and dense retrieval both benefit without retriever-side changes. One prefix string, two retrievers fixed.
2. The cross-encoder also sees the prefix at rerank time, so the title context flows into the rescoring decision too.
3. It's reversible: drop the prefix in display by stripping the known format.

The prefix lives in `chunk.text` directly. The chunk's metadata still carries `title` and `section_heading` as fields for filtering and citation rendering, but the searchable text is what the retrievers actually score against.

### Numbers

Overall Recall@5: 0.310 → 0.517. Per-type, the lifts went where I expected and one place I didn't:

- contribution_recall: 0.333 → 1.000 (perfect). "What are the contributions of <paper>" now matches because the title is in every chunk of that paper.
- cross_paper: 0.000 → 1.000 (perfect). Surprise. The chunks now disambiguate which paper they came from at the embedding layer, so cross-paper queries that name both papers retrieve from both. I had predicted this category would need an agent layer; for the two specific cross-paper questions in the eval set, the embedding gain was enough.
- methodology: 0.000 → 0.500. Section heading prefix helps "how did they do X" find the methods section.
- table_numerical: 0.000 → 0.000. The cross-encoder still doesn't rerank table-format chunks well (model fit, not pool depth). The fix here is a different reranker or table-aware chunking, neither of which the prefix touches.
- multi_hop / vague_ambiguous: 0.000. Still agent-layer problems, as expected.

I bumped CHUNKER_VERSION from 2 to 3. The change invalidates `config_hash`, which forces the ingest pipeline to re-process the whole corpus under the new chunking. Without the bump the dedup check would have skipped re-ingest and v4 would have run against v3 chunks.

---

## Widened RERANK_TOP=50 (v5)

v4 fixed the deep failures by getting the right chunks into the candidate pool. Next question: does a wider rerank pool help? The cross-encoder was rescoring the top-20 of the fused result. If gold chunks are landing at ranks 21 through 50 in the fused output, widening the pool would catch them.

I widened RERANK_TOP from 20 to 50 and re-ran. Strict Recall@5 stayed at 0.517. Per-question diffs were small and went both ways. The change wasn't moving the rank-1 metric.

But the LLM-judged metrics moved:

- context_recall: +0.133
- faithfulness: +0.037

This is the latent-quality signal. The strict chunk_id match doesn't reward "the gold chunk wasn't returned but a different chunk with the answer text was". The LLM-judged metrics do. Widening the rerank pool was pulling in adjacent chunks containing the answer content without matching the gold chunk_id. The minimal generator answered more questions correctly with the wider pool's top-5.

I kept RERANK_TOP=50. The cost is one cross-encoder pass on 50 instead of 20 candidates (about 25 ms more per query on CPU). The benefit is measurable on the metrics that reflect downstream answer quality.

---

## Structural cleanup

Through v1 to v5 the repo accumulated leftovers from the AMD-demo origin. Before wrapping with MCP I cleaned the structure so the library boundary is clear.

### tools/ to mini_rag/

The library was at `tools/`. Generic name, not what the project is. I renamed via `git mv` to preserve history, then mass-updated 9 files' imports from `from tools.X` to `from mini_rag.X`. The library is now `mini_rag`, the dev CLI is in `scripts/`, the tests are in `tests/`. Standard layout.

### Dev agent moved out of the library

`agent.py` and `main.py` were at the project root. They wired the LangChain ReAct agent for local interactive testing. That's dev tooling, not library code. I consolidated them into `scripts/dev_agent.py`. The banner changed from "AMD Knowledge Assistant" to "Mini-RAG dev agent" and the system prompt was rewritten for research-paper context.

The dev agent stays in the repo because it's still useful for sanity-checking changes without spinning up an MCP client. I considered deleting it; the MCP server is the production interface and would be enough on its own. I kept the dev agent because it exercises the LangChain side of the stack, which recruiters mention in JDs. Two interfaces, same retrieval underneath.

### Config consolidation

`scripts/sourcing/config.py` and root `config.py` were two separate config files for different parts of the pipeline. The sourcing config held arxiv categories and date ranges; the root config held everything else. I merged them: the sourcing constants moved into root `config.py` with a `SOURCING_*` prefix. `fetch_papers.py` now imports `SOURCING_CATEGORIES`, `SOURCING_MAX_RESULTS`, etc. from the consolidated root.

Every config value also now supports an environment-variable override using the pattern `os.environ.get("VAR", default)`. This matters for MCP deployment: the consumer sets `INGEST_CORPUS_DIR` or `RERANK_TOP` in their MCP client config without forking the repo.

### Smoke tests deleted

`tests/test_ingest.py` and `tests/test_retriever.py` were initial smoke tests written before the eval framework existed. The eval runner at `tests/eval/run_eval.py` now exercises the full ingest-to-retrieve path across 30 questions with deterministic and LLM-judged metrics. The smoke tests were exercising the same code paths with less coverage. I deleted them.

The instinct to keep "extra tests just in case" is wrong here. Tests have a maintenance cost and the eval framework already covers what they covered. The cleaner state is the right call.

---

## MCP wrapper

The retrieval pipeline is now stable and the eval numbers are documented. Time to expose it.

### Why MCP and not a Skill

Anthropic's Claude has two extension mechanisms: MCP servers (external tools and resources) and Skills (workflow extensions baked into Claude). They occupy different layers:

- MCP is the data and service layer. It exposes capabilities that need code execution: search a vector store, call an API, query a database. Available to any MCP-compatible client.
- Skills are the workflow layer. They package a recipe for how to use existing capabilities. They run inside Claude.

A RAG system is fundamentally a service. It owns code, indices, and a corpus. MCP fits. A skill that "uses Mini-RAG" would still need MCP underneath to actually retrieve anything. Both can coexist: someone could write a Skill that wraps the MCP tools with a domain-specific prompt, but the MCP server is the necessary substrate.

I went with MCP. The skill layer can come later if the use case calls for it.

### The tool surface

Four tools, five resources. The split is deliberate:

- Tools are actions: `search_knowledge(query, k)`, `list_corpus()`, `ingest_new_documents()`, `ingest_from_arxiv(arxiv_id)`. The first two are read-side; the last two are write-side.
- Resources are read-only data: `eval://golden_set`, `eval://latest_results`, `eval://baseline_analysis`, `eval://v4_per_question_diagnosis`, `corpus://manifest`.

I considered exposing the `eval://*` data as tools instead. Two reasons I kept them as resources: they don't take arguments, and they don't change state. MCP resources are the right primitive for "here's a chunk of data clients can read". Tools are the right primitive for "here's a thing clients call". Mixing them by exposing read-only data as zero-argument tools muddles the contract.

`ingest_from_arxiv` exists because a consumer agent might want to add a paper on demand. The implementation downloads the PDF, updates the corpus manifest with metadata, and reuses the standard ingest pipeline. Idempotent: dedup on `arxiv_id + config_hash` skips already-ingested papers.

### Deploy-time configuration only

I considered exposing a `configure(...)` tool that lets the consumer change retrieval parameters at runtime. I dropped it. The consumer should set `RERANK_TOP`, `TOP_K`, `INGEST_CORPUS_DIR` in their MCP client config (env vars) and restart the server. Reasons:

- Runtime config negotiation is a stateful concern. The server would have to track per-client state.
- The config values are deployment knobs, not per-query knobs. Per-query knobs like `k` are already on `search_knowledge`.
- It's harder to reproduce an eval run when the server's behavior depends on prior client interactions.

The env-var override pattern from the config consolidation makes deploy-time tuning trivial without touching code.

### check_setup

I added `mini_rag/check_setup.py` as a separate utility. It runs through a checklist (API key, corpus dir, Chroma reachable, MCP server importable, vector store collection populated) and reports green or red per item. It's the answer to "I cloned this and it doesn't work". One command tells you what's missing.

It isn't part of the MCP server itself because the MCP server has a different concern (be a server). The setup checker is for the human who just cloned the repo.

---

## GPU acceleration: considered, deferred

SPECTER2 embedding is the bottleneck of the ingest pipeline. On a 7400-chunk corpus, embedding takes 15-20 min on CPU and would drop to 1-2 min on a consumer NVIDIA GPU. The same speedup applies to Docling's layout model if it gets pointed at the GPU too. Overall ingest could go from ~30 min to ~5 min. Real win on paper.

The runtime side is trivial: one line in the embedding code to read `os.environ.get("DEVICE")` and pass it to `SentenceTransformer(model, device=device)`. sentence-transformers auto-detects if you don't specify, so a CUDA-enabled torch install just works.

The install side is where it falls apart. PyTorch's CUDA wheels don't live on PyPI; they live on `download.pytorch.org/whl/cu124` (and `cu121`, `cu118`, etc.). The wheel has to match the user's CUDA driver version. There's no way to do this cleanly inside `pyproject.toml` without either:

- forcing every user to know their CUDA version and pick a uv dependency group (`uv sync --group gpu` plus a `[tool.uv.sources]` block pinning torch to the right pytorch.org index), or
- writing a custom install script that runs `nvidia-smi`, parses the driver version, picks the right wheel, and pip-installs it.

I considered the install-script path. It's 50-80 lines of subprocess plumbing with a long tail of edge cases (`nvidia-smi` not on PATH on Windows, WSL2 reporting differently, multiple GPUs, AMD ROCm, Apple MPS, and the case where torch reports installed but a DLL load error means it actually doesn't work). The script handles the simple cases and bails on everything else, which means the user who actually has a problem still has to debug manually. The 50 lines don't buy them much.

A custom install script also reads wrong for a portfolio repo. Auto-install scripts are conventional for full end-user applications (ComfyUI, oobabooga, AUTOMATIC1111). They're not conventional for libraries. A reviewer expecting `uv sync` would side-eye a project that runs subprocess + downloads wheels on first install.

So GPU support stays out of the default install path. The CPU baseline runs anywhere a reviewer might clone it. Anyone with a GPU who wants the speedup pays the standard ML-ecosystem cost: install a CUDA-enabled torch themselves the way they already know how. If I ever scale the corpus past a few hundred papers, this calculation flips and the dependency-group path becomes worth wiring up. Not at 50 papers.

---

## Future Improvements

**Table-aware chunking and reranking.** v5 left `table_numerical` at 0.000. The MS-MARCO MiniLM cross-encoder doesn't score table-row chunks well, and the current chunker splits tables into per-row pieces via Docling's structured output. Two threads to pull on: keep each table as one chunk (caption plus rows joined, conflicts with the size ceiling so needs a separate code path), or swap in a reranker trained on tabular content.

**Parent-document retrieval.** Index small chunks for embedding precision, return larger parent sections to the LLM for context. Should lift context_recall further. Schema is already forward-compatible (chunk metadata can carry parent IDs).

**Agent-layer query decomposition for multi-hop and vague queries.** The eval surfaced these as outside the RAG's scope. They belong in the MCP-consuming agent layer that decomposes a complex question into sub-queries, calls `search_knowledge` for each, and synthesizes the results.

**Document preprocessing agent.** An agent that inspects each incoming document and routes it to the right parser (Docling for digital PDFs, OCR for scanned, structured table parser, slide parser). Replaces the fixed `parse_document` with adaptive routing.

**Semantic chunking as a phase-later option.** Currently deferred because docling's structural chunks were good enough and semantic chunking adds embedding cost. Worth revisiting if the eval shows specific failure modes that paragraph-level chunking can't address.

**Tracing and cost tracking.** Wire Langfuse or Phoenix for per-request tracing during retrieval and generation. Useful both for debugging and for quantifying the per-query cost as the system scales.

**Local LLM swappable for generation.** Add a switchable backend so the generation step (and potentially the RAGAS judge calls) can run against a local model. Useful for the privacy-aware use case and lowers eval cost during iteration.
