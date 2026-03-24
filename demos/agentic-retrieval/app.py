# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anthropic",
#     "scikit-learn",
#     "pyyaml",
#     "prompt-toolkit",
#     "python-dotenv",
# ]
# ///
"""
Agentic Document Retrieval Demo — Context Engineering Hands-On

Run: uv run app.py

This demo shows how context flows through an agent loop with retrieval tools.
Watch the messages array grow, observe tool calls injecting documents into
context, and understand the token cost of each decision.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout

# Load .env file if present (does not override existing env vars)
load_dotenv()

# Ensure local imports work when run via `uv run`
sys.path.insert(0, str(Path(__file__).parent))

import display
from agent import Agent
from retrieval import KnowledgeBase


HISTORY_FILE = Path(__file__).parent / ".chat_history"


def handle_slash_command(command: str, agent: Agent) -> bool:
    """
    Handle slash commands. Returns True if a command was handled.
    """
    cmd = command.strip().lower()

    if cmd == "/help":
        display.welcome_banner()
        return True

    elif cmd == "/context":
        messages = agent.get_context_snapshot()
        if not messages:
            display.system_message("Context is empty — start a conversation first.")
        else:
            display.context_snapshot(messages)
        return True

    elif cmd == "/stats":
        stats = agent.get_stats()
        if stats.turn_count == 0:
            display.system_message("No stats yet — start a conversation first.")
        else:
            display.context_stats(
                turn_count=stats.turn_count,
                message_count=len(agent.get_context_snapshot()),
                tool_call_count=stats.tool_call_count,
                input_tokens=stats.total_input_tokens,
                output_tokens=stats.total_output_tokens,
            )
        return True

    elif cmd == "/clear":
        agent.clear_context()
        display.system_message("✓ Context cleared — messages and stats reset.")
        return True

    elif cmd == "/docs":
        docs = agent.kb.list_documents()
        display.system_message(f"Knowledge base: {len(docs)} document(s)\n")
        for d in docs:
            display.system_message(
                f"  • {d['id']}: {d['title']} (~{d['token_estimate']} tokens)"
            )
        print()
        return True

    elif cmd in ("/quit", "/exit", "/q"):
        display.system_message("Goodbye!")
        sys.exit(0)

    return False


def main() -> None:
    """Main entry point — interactive prompt loop."""
    # Initialize knowledge base and agent
    kb = KnowledgeBase()
    agent = Agent(kb)

    display.welcome_banner()

    session: PromptSession = PromptSession(
        history=FileHistory(str(HISTORY_FILE)),
    )

    while True:
        try:
            with patch_stdout():
                user_input = session.prompt("\n  You: ").strip()
        except (KeyboardInterrupt, EOFError):
            display.system_message("\nGoodbye!")
            break

        if not user_input:
            continue

        # Check for slash commands
        if user_input.startswith("/"):
            if not handle_slash_command(user_input, agent):
                display.error(f"Unknown command: {user_input}. Try /help")
            continue

        # Run the agent turn
        try:
            response = agent.run_turn(user_input)
            display.assistant_text(response)
        except Exception as e:
            display.error(f"Agent error: {e}")


if __name__ == "__main__":
    main()
