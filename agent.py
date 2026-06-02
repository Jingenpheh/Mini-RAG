from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import LLM_MODEL, LLM_TEMPERATURE
from tools import all_tools


# --- System prompt ---
# Defines the agent's personality, rules, and behavior.
# This is sent to the LLM with every API call as the system message.

SYSTEM_PROMPT = """You are an AMD knowledge assistant. You have access to a knowledge \
base of AMD documents and can have normal conversations with users.

## How to handle AMD-related questions
1. Always search the knowledge base first using search_knowledge_tool.
2. When searching, use specific technical terms rather than conversational language.
3. If the user's question is long or vague, extract the core intent and search for that.
4. If search results don't clearly answer the question, try rephrasing your query and search again (max 2 retries).
5. If results are still insufficient, call ingest_documents_tool to check for new documents in the docs/ folder.
6. After ingesting, search again.

## Grounding rule
- When you answer using information from the knowledge base, cite the source document and page.
- If the knowledge base does not contain the answer but you have general knowledge that \
might help, you MAY share it — but you MUST clearly label it like this:
  "Note: This is based on my general knowledge, not from the documents in the knowledge base."
- Never mix sourced and unsourced information without clearly distinguishing them.

## General conversation
- You can handle greetings, small talk, and non-AMD questions naturally.
- You don't need to search the knowledge base for casual conversation.

## Citations
- Always cite which document and page when using retrieved information.
- Use the source metadata returned by the search tool.

## Tone
- Professional but conversational.
- Concise answers with specific details from the source documents."""


# --- Prompt template ---
# Defines the message structure sent to the LLM on every call.
# Order matters: system rules first, then conversation history,
# then the current question, then the agent's working memory (scratchpad).

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder("chat_history"),          # Previous conversation turns (persists across turns)
    ("human", "{input}"),                         # Current user message
    MessagesPlaceholder("agent_scratchpad"),       # Agent's tool calls and results (within current turn only)
])


# --- LLM ---
llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)


# --- Agent ---
# create_tool_calling_agent: creates the agent "brain" — decides which tool to call
# AgentExecutor: runs the ReAct loop (think → act → observe → repeat) until the agent produces a final answer

agent = create_tool_calling_agent(llm, all_tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=all_tools,
    verbose=True,       # Prints agent thinking and tool calls to console — useful for demo
)
