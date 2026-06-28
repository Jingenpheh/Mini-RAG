"""Mini-RAG dev agent: interactive LangChain ReAct loop for local testing.

This is a developer convenience, not a production interface. The production
interface to Mini-RAG is the MCP server (mini_rag/mcp_server.py). Use this
dev agent to:

  - Manually verify retrieval quality against a query you have in mind.
  - Test the ingest tool against a freshly-dropped PDF.
  - Smoke-test agent behavior changes (system-prompt experiments).

Run from the project root:

    python -m scripts.dev_agent

The agent uses LangChain's create_tool_calling_agent. Tools wrap the same
retrieve() and ingest_documents() functions that the MCP server exposes,
so what you see here approximates what a consumer agent would see when
calling Mini-RAG via MCP.
"""

# Load environment variables (.env) before any other imports so OPENAI_API_KEY
# is available when LangChain initializes.
from dotenv import load_dotenv
load_dotenv()

import sys
from pathlib import Path

# Add the project root to sys.path so we can import from mini_rag and config.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from langchain_openai import ChatOpenAI                              # noqa: E402
from langchain.agents import create_tool_calling_agent, AgentExecutor  # noqa: E402
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # noqa: E402

from config import LLM_MODEL, LLM_TEMPERATURE                        # noqa: E402
from mini_rag import all_tools                                       # noqa: E402


# ##############################################################################
# System prompt
# ##############################################################################

SYSTEM_PROMPT = """You are Mini-RAG, a research-paper knowledge assistant. \
You have access to a knowledge base of arXiv ML/AI papers and can have \
normal conversations with users.

## How to handle research-paper questions

1. Always search the knowledge base first using search_knowledge_tool.
2. When searching, use specific technical terms (system names, acronyms,
   distinctive method names) rather than conversational language.
3. If the user's question is long or vague, extract the core intent and
   search for that.
4. If search results don't clearly answer the question, try rephrasing
   your query and search again (max 2 retries).
5. If results are still insufficient, call ingest_documents_tool to check
   for new documents in the docs/ folder, then search again.

## Grounding rule

- When you answer using information from the knowledge base, cite the
  source paper by arXiv ID and section heading.
- If the knowledge base does not contain the answer but you have general
  knowledge that might help, you MAY share it, but you MUST clearly label
  it like this:
    "Note: This is based on my general knowledge, not from the documents
    in the knowledge base."
- Never mix sourced and unsourced information without clearly
  distinguishing them.

## General conversation

- You can handle greetings, small talk, and meta questions about the
  knowledge base naturally.
- You don't need to search the knowledge base for casual conversation.

## Citations

- Always cite which paper and section when using retrieved information.
- Use the arxiv_id and section_heading returned by the search tool.

## Tone

- Professional but conversational.
- Concise answers with specific details from the source papers."""


# ##############################################################################
# Prompt template
# ##############################################################################

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])


# ##############################################################################
# Agent + executor
# ##############################################################################

llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
agent = create_tool_calling_agent(llm, all_tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=all_tools,
    verbose=True,
)


# ##############################################################################
# Interactive REPL
# ##############################################################################


def main() -> None:
    """Interactive REPL for the dev agent."""

    print("Mini-RAG dev agent  (type 'quit' to exit)")
    print("=" * 50)

    chat_history = []

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        result = agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history,
        })

        answer = result["output"]
        print(f"\nAssistant: {answer}")

        chat_history.append(("human", user_input))
        chat_history.append(("ai", answer))


if __name__ == "__main__":
    main()
