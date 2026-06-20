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

## Future Improvements

**Semantic chunking.** Use a local embedding model to find meaning boundaries instead of character boundaries, which avoids per-window API cost.

**Document preprocessing agent.** An agent sitting before the embedding pipeline that inspects each document and routes it to the right parser (text extraction, OCR, or structural parsing), replacing the fixed pipeline.

**Re-ranking.** After initial retrieval, rescore results with a cross-encoder model to filter out chunks that are semantically close but topically off.

**Query reformulation.** Generate multiple query variants per search using LangChain's `MultiQueryRetriever`, then merge and deduplicate results.

**Evaluation framework.** Automated retrieval and answer evaluation using RAGAS or LangChain's eval tools. Key metrics are faithfulness (answer matches sources), relevance (chunks match query), and completeness (all aspects addressed). Agent tool usage patterns are also worth tracking, to check whether the agent is choosing the right tool for each situation.
