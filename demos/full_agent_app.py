# /// script
# requires-python = ">=3.12"
# dependencies = ["claude-agent-sdk", "python-dotenv"]
# ///
"""
Simplified agentic-RAG CLI.

A chat app where Claude has three custom tools for working with a folder of
.md files: list them, read one, or search across them. The agent decides
when to call which tool — you just ask questions.

Usage:
  uv run demos/full_agent_app.py
  uv run demos/full_agent_app.py path/to/folder
"""

import sys
import anyio
from pathlib import Path
from dotenv import load_dotenv
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    tool,
    create_sdk_mcp_server,
)

load_dotenv()

# ---------------------------------------------------------------------------
# access to documents
# ---------------------------------------------------------------------------
DEFAULT_KB = Path(__file__).parent / "agentic-retrieval" / "knowledge_base"
KB_PATH = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_KB.resolve()


def _md_files() -> list[Path]:
    return sorted(KB_PATH.glob("*.md"))


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------
@tool("list_docs", "List all .md files available in the knowledge base.", {})
async def list_docs(_args: dict) -> dict:
    files = [p.name for p in _md_files()]
    body = "\n".join(f"- {name}" for name in files) or "(no .md files found)"
    return {"content": [{"type": "text", "text": body}]}


@tool(
    "read_doc",
    "Read the full contents of a .md file from the knowledge base by filename.",
    {"filename": str},
)
async def read_doc(args: dict) -> dict:
    path = KB_PATH / args["filename"]
    if not path.is_file() or path.suffix != ".md" or path.parent != KB_PATH:
        return {"content": [{"type": "text", "text": f"File not found: {args['filename']}"}]}
    return {"content": [{"type": "text", "text": path.read_text()}]}


@tool(
    "search_docs",
    "Search across all .md files for a query. Returns matching files with a snippet.",
    {"query": str},
)
async def search_docs(args: dict) -> dict:
    query = args["query"].strip()
    if not query:
        return {"content": [{"type": "text", "text": "Empty query."}]}

    q_lower = query.lower()
    q_tokens = [t for t in q_lower.split() if len(t) > 2]

    results: list[tuple[str, int, str]] = []
    for path in _md_files():
        text = path.read_text()
        text_lower = text.lower()
        phrase_hits = text_lower.count(q_lower)
        token_hits = sum(text_lower.count(t) for t in q_tokens)
        score = phrase_hits * 5 + token_hits
        if score == 0:
            continue
        anchor = text_lower.find(q_lower)
        if anchor == -1:
            anchor = next((text_lower.find(t) for t in q_tokens if t in text_lower), 0)
        start = max(0, anchor - 80)
        end = min(len(text), anchor + 200)
        snippet = ("…" if start else "") + text[start:end].strip() + ("…" if end < len(text) else "")
        results.append((path.name, score, snippet))
    results.sort(key=lambda r: r[1], reverse=True)

    if not results:
        return {"content": [{"type": "text", "text": f"No matches for '{query}'."}]}

    results_text = "\n\n".join(
        f"## {name} (score={score})\n{snippet}" for name, score, snippet in results[:5]
    )
    return {"content": [{"type": "text", "text": results_text}]}


# ---------------------------------------------------------------------------
# Agent code
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = f"""\
You are a research assistant with access to a knowledge base of markdown notes
located at: {KB_PATH}

You have three tools:
  - list_docs:   see what files are available
  - search_docs: find files relevant to a query (use this first for most questions)
  - read_doc:    pull the full contents of a specific file into context

Strategy: search first to find candidates, then read the most promising 1-2
files in full before answering. Cite filenames in your answer. Be concise.
"""

docs_server = create_sdk_mcp_server(
    name="docs",
    version="1.0.0",
    tools=[list_docs, read_doc, search_docs],
)

OPTIONS = ClaudeAgentOptions(
    model="claude-sonnet-5",
    system_prompt=SYSTEM_PROMPT,
    mcp_servers={"docs": docs_server},
    allowed_tools=[
        "mcp__docs__list_docs",
        "mcp__docs__read_doc",
        "mcp__docs__search_docs",
    ],
    max_turns=10,
)


# ---------------------------------------------------------------------------
# Some way of displaying the information
# ---------------------------------------------------------------------------
async def stream_response(client: ClaudeSDKClient) -> None:
    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    args_preview = ", ".join(f"{k}={v!r}" for k, v in block.input.items())
                    print(f"  \033[90m[tool] {block.name}({args_preview})\033[0m", flush=True)
                elif isinstance(block, TextBlock):
                    print(f"\n\033[36mAssistant:\033[0m {block.text}\n", flush=True)


# ---------------------------------------------------------------------------
# Wrap into simple cli chat based app
# ---------------------------------------------------------------------------
async def main() -> None:
    if not KB_PATH.is_dir():
        print(f"Knowledge base folder not found: {KB_PATH}")
        sys.exit(1)

    print(f"\n\033[1mAgentic RAG over:\033[0m {KB_PATH}")
    print(f"\033[1mFiles:\033[0m {len(_md_files())} .md files")
    print("Type a question — 'exit' to quit.\n")

    async with ClaudeSDKClient(options=OPTIONS) as client:
        while True:
            try:
                user_input = input("\033[33mYou:\033[0m ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                break

            await client.query(user_input)
            await stream_response(client)


if __name__ == "__main__":
    anyio.run(main)
