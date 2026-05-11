# /// script
# requires-python = ">=3.12"
# dependencies = ["claude-agent-sdk"]
# ///
"""
Repo Q&A agent — answers questions about this course repo.

Usage:
  uv run agent_tool_for_claude_code.py "where is the agentic retrieval demo?"
  uv run agent_tool_for_claude_code.py "what context failure modes does session 3 cover?"
"""

import sys
import anyio
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

REPO_ROOT = str(Path(__file__).resolve().parent.parent.parent)

SYSTEM_PROMPT = """\
You are a knowledgeable assistant for the 'Context Engineering Hands-On' O'Reilly course repo.

The course teaches developers how to design, manage, and optimize the context flowing into LLMs and agentic systems across 5 sessions:
1. Introduction to Context Engineering
2. Engineering Context in Agentic Systems
3. Diagnosing and Fixing Context Failures
4. Context Engineering Patterns in Modern AI Apps
5. Tools and Techniques for Modern Development

Answer questions about file locations, document content, and context engineering concepts in the repo.
Be concise and direct. Always include file paths when relevant."""


async def main():
    if len(sys.argv) < 2:
        print("Usage: uv run agent_tool_for_claude_code.py '<your question>'")
        sys.exit(1)

    question = " ".join(sys.argv[1:])

    async for message in query(
        prompt=question,
        options=ClaudeAgentOptions(
            cwd=REPO_ROOT,
            allowed_tools=["Read", "Glob", "Grep"],
            system_prompt=SYSTEM_PROMPT,
            max_turns=15,
        ),
    ):
        if isinstance(message, ResultMessage):
            print(message.result)


anyio.run(main)
