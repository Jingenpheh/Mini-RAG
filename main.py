# Load environment variables (.env file) before any other imports
# This must happen first so the OpenAI API key is available when agent.py initializes
from dotenv import load_dotenv
load_dotenv()

from agent import agent_executor


def main():
    print("AMD Knowledge Assistant (type 'quit' to exit)")
    print("=" * 50)

    # Chat history stores previous turns so the agent remembers the conversation
    # Each entry is a (role, message) tuple — we manage this ourselves
    chat_history = []

    while True:
        user_input = input("\nYou: ").strip()

        # Skip empty input
        if not user_input:
            continue

        # Exit commands
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        # Invoke the agent — this triggers the ReAct loop internally
        # The agent decides which tools to call based on the input and prompt
        result = agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history,
        })

        # Extract and display the agent's final answer
        answer = result["output"]
        print(f"\nAssistant: {answer}")

        # Append this turn to chat history for conversation memory
        # Only the clean Q&A is stored — agent scratchpad (tool calls) is not included
        chat_history.append(("human", user_input))
        chat_history.append(("ai", answer))


if __name__ == "__main__":
    main()
