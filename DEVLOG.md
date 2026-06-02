# Mini-RAG — Development Log

## Project Goal

Build a minimal RAG agent on OpenAI + LangChain + ChromaDB to get hands-on familiarity with the LangChain framework and explore RAG pain points in practice.

---

## Architecture & Project Structure

This project is small — everything could fit in a single `main.py`. But even for a small project, we should follow standard engineering practices for how the repo is structured: separating configuration, tools, agent logic, and the entry point into their own modules.

The tools folder splits ingestion and retrieval into independent files that don't depend on each other. They share a common utility (`get_vector_store()` in `utils.py`) for connecting to Chroma, but beyond that they're decoupled. This means each piece is testable on its own — we wrote smoke tests for ingestion and retrieval independently before ever wiring them into the agent.

The agent itself has three tools: `search_knowledge`, `ingest_documents`, and `list_sources`. Rather than a fixed retrieve→generate pipeline, the agent decides which tool to call and when. This makes it genuinely agentic — it reasons about whether to search, ingest new documents, or simply respond based on the conversation.

---

## RAG System

### Chunking

The first thing to figure out in any RAG system is how to chunk the documents. We considered several approaches: fixed character splits, sentence-level splits, paragraph splits, recursive character splitting, and semantic chunking.

Semantic chunking would be the strongest option — it uses an embedding model to detect meaning boundaries, so chunks align with actual topic shifts. But it requires an embedding call per sliding window, adding cost and latency. For a small corpus of blog posts, that overhead isn't justified.

We went with **RecursiveCharacterTextSplitter** (500 characters, 100 character overlap). It tries paragraph breaks first, then falls back to sentence boundaries, then words — so chunks stay semantically coherent without needing a model. The 20% overlap ensures that if an idea spans a chunk boundary, it's captured in both chunks.

This is a pragmatic starting point. If retrieval quality becomes an issue at scale, semantic chunking with a local embedding model (avoiding per-window API cost) would be the next step to explore.

### Corrective RAG

One concern with any RAG system is that the retrieved chunks might not actually answer the question — similarity search returns "similar" text, not necessarily "relevant" text. In some architectures, a separate evaluation step sits between retrieval and generation: an LLM checks whether the chunks are useful before the main agent generates an answer.

We considered this but realized the agent already handles it naturally through the ReAct loop. When the agent receives search results, it reads them and reasons about whether they answer the question. If they don't, the system prompt instructs it to rephrase the query and try again (up to 2 retries), then check for new documents to ingest. This is effectively corrective RAG — implemented through prompt engineering rather than a separate evaluation component.

The advantage is simplicity: no extra LLM calls, no separate evaluation chain. The tradeoff is less control — we're relying on the agent's judgment rather than an explicit quality check. For this project that's fine. For a production system with higher accuracy requirements, an explicit evaluation step (using something like RAGAS) would be more reliable.

### Document Parsing — Issues and Ideas

Document parsing turned out to be one of the most interesting challenges. Three issues surfaced during development:

First, some PDFs saved from Chrome were image-based — PyPDFLoader returned zero characters because there was no text layer, only page screenshots. We re-saved the PDFs to fix it, but this revealed a deeper problem: you can never assume a PDF has extractable text.

Second, even text-layer PDFs came out with messy formatting — one word per line, excessive spacing. We added a cleanup step (`re.sub(r"\s+", " ", text)`) before chunking to collapse whitespace into readable text.

Third, PDFs from web pages included navigation bars, footers, "Share on LinkedIn" buttons, and cookie banners — all of which got chunked and embedded alongside meaningful content. For a small corpus the noise is manageable, but at scale it would waste retrieval slots.

These issues led us to think about what a more robust solution would look like. A fixed parsing pipeline (always use PyPDF, always clean with regex) breaks the moment you encounter a document it wasn't designed for. Different documents need different strategies: text extraction for digital PDFs, OCR for scanned documents, structural parsing for documents with tables or complex layouts.

One idea that came up was a **document preprocessing agent** — an agent that sits before the embedding pipeline, inspects each incoming document, and routes it to the appropriate parser. It would detect whether a PDF has a text layer or needs OCR, whether the content has boilerplate that should be stripped, whether tables need special handling. This turns document preprocessing into an agentic task rather than a hardcoded pipeline, making it adaptive to whatever comes in.

We didn't build this — it's beyond scope for a small project — but it's a direction worth exploring for a production RAG system.

---

## Agent Design

We used the **ReAct** (Reasoning + Acting) pattern via LangChain's `create_tool_calling_agent`. Other patterns exist — Plan-and-Execute for long-horizon tasks with many sequential steps, Reflection/Self-RAG for self-correcting systems, multi-agent architectures for complex multi-domain workflows. ReAct fits here because knowledge retrieval is a short-horizon task: search, observe the results, decide if more action is needed, answer. No long-range planning required.

One thing worth noting about how LangChain agents work under the hood: the LLM doesn't know it's inside a framework. On every API call, LangChain sends the tool definitions (name, description, parameter schema) alongside the conversation as a JSON payload. The LLM was trained to understand this format and respond with structured tool calls. This is why tool descriptions matter — they're not comments for developers, they're instructions the LLM reads on every single call to decide which tool to use and what arguments to pass.

### A note on MCP (Model Context Protocol)

During development we looked into whether MCP was relevant here. MCP standardizes how tools are exposed and discovered across applications — think of it as a marketplace where tools are registered once and any MCP-compatible client can find and use them.

In this project, our tools are defined directly in Python and only used by our own agent, so MCP adds no value. But the picture changes in a larger setting: imagine a company where multiple departments build their own AI agents, and people use different interfaces — VS Code, Claude Code, Cursor, a custom web UI. Without MCP, every tool has to be re-implemented or wrapped for each interface. With an MCP server, tools are defined once and any compatible client can discover and call them.

So MCP makes sense when you don't control all the interfaces consuming your tools, or when tools need to be shared across teams and applications. For a self-contained project like this where we define both the tools and the agent that uses them, LangChain's native tool system is sufficient.

---

## System Prompt — Iteration Log

The system prompt went through three iterations, and this turned out to be one of the more insightful parts of the project.

**v1 — Too loose:** The prompt said "don't hallucinate." When asked about AMD gaming (not in the knowledge base), the agent searched, found nothing relevant, then responded with detailed information about Radeon RX and ray tracing from its training data — with no indication that this wasn't from the knowledge base. This defeats the entire purpose of RAG: if the agent freely falls back to training data without telling you, you can't trust which parts of any answer are grounded.

**v2 — Too strict:** We overcorrected to "NEVER generate information not returned by your tools." The agent refused everything — even "hi there" got "I don't have information about that in my knowledge base." It became an unintelligent search terminal with no conversational ability.

**v3 — Balanced (current):** The agent can converse naturally and use general knowledge, but must clearly label what's from the knowledge base vs what's not. AMD questions always search first. If the knowledge base doesn't have the answer, the agent can share general knowledge but must add a disclaimer. The goal is transparency, not restriction — a good RAG assistant distinguishes sourced from unsourced information rather than refusing to speak.

---

## Stack Choices

- **LLM: GPT-4o-mini** — cheapest OpenAI model with solid tool-calling. Temperature=0 for deterministic, grounded answers.
- **Embeddings: text-embedding-3-small** — already on the same OpenAI API key, so no additional provider needed. Higher quality than Chroma's default local model.
- **Vector store: ChromaDB** — runs in-process with zero infrastructure (SQLite under the hood). Pinecone needs a cloud account, pgvector needs PostgreSQL, FAISS has no metadata filtering. Chroma is the simplest option for a local project.
- **Framework: LangChain** — more flexible for agent orchestration than LlamaIndex, which is more opinionated about the RAG pipeline itself. This project is agent-first (retrieval is one tool among several), so LangChain's flexibility is the better fit.

---

## Testing Summary

**Ingestion:** 3 documents → 50 chunks. Deduplication verified (second run skips existing docs). Incremental ingestion works (only new PDFs processed). Empty chunk filtering and text cleaning verified.

**Retrieval:** Text accuracy 100% against source documents. Relevance ~75% — some queries return tangentially related chunks. Embedding similarity captures semantic closeness but not always topical precision.

**Agent:** Searches before answering. Rephrases on insufficient results. Ingests when prompted. Handles casual conversation. Labels unsourced information with disclaimers. Cites documents and page numbers.

---

## Future Improvements

**Semantic chunking:** Use a local embedding model to find meaning boundaries rather than character boundaries, avoiding per-window API cost.

**Document preprocessing agent:** An agent that inspects incoming documents and routes to the appropriate parser — text extraction, OCR, or structural parsing — instead of a fixed pipeline.

**Re-ranking:** After initial retrieval, rescore results with a cross-encoder model to filter out chunks that are semantically similar but not topically relevant.

**Query reformulation:** Generate multiple query variants per search using LangChain's `MultiQueryRetriever`, then merge and deduplicate results.

**Evaluation framework:** Automated retrieval and answer evaluation using RAGAS or LangChain's eval tools. Key metrics: faithfulness (answer matches sources), relevance (chunks match query), completeness (all aspects addressed). Also track agent tool usage patterns — is it choosing the right tool for each situation?
