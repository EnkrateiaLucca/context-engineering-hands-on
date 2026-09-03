# Agentic Document Retrieval Demo

A hands-on demo showing how context flows through an agent loop with retrieval tools. Built for Session 2 of the Context Engineering course.

## Architecture

```
┌──────────────────────────────────────────────┐
│  app.py (TUI + slash commands)               │
│  ┌────────────────────────────────────────┐  │
│  │  agent.py (agent loop)                 │  │
│  │  ┌──────────┐  ┌───────────────────┐  │  │
│  │  │ messages  │  │  Anthropic API    │  │  │
│  │  │ array     │←→│  (Claude Sonnet)  │  │  │
│  │  │ (context) │  └───────────────────┘  │  │
│  │  └────┬─────┘                          │  │
│  │       │ tool calls                     │  │
│  │  ┌────▼─────────────────────────────┐  │  │
│  │  │  tools.py → retrieval.py         │  │  │
│  │  │  (TF-IDF over knowledge_base/)   │  │  │
│  │  └──────────────────────────────────┘  │  │
│  └────────────────────────────────────────┘  │
│  display.py (ANSI output)                    │
└──────────────────────────────────────────────┘
```

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- `ANTHROPIC_API_KEY` environment variable set

## Quick Start

```bash
# Run the main demo
uv run app.py
```

No virtual environment or `pip install` needed — uv handles dependencies automatically.

## Suggested Query Sequence

Try these queries in order to see context grow across turns:

1. **"What documents do you have?"** → triggers `list_documents` tool
2. **"What is context engineering?"** → triggers `search_documents`, returns grounded answer
3. **"Tell me more about the Manus architecture"** → triggers `get_document` for full content
4. **"How does RAG relate to what Manus does?"** → multi-doc synthesis, observe token growth
5. Run `/context` → inspect the raw messages array
6. Run `/stats` → see cumulative token counts
7. **"Summarize everything we've discussed"** → large input context, high token cost
8. Run `/clear` → reset and compare fresh vs accumulated context cost

## Slash Commands

| Command    | Description |
|------------|-------------|
| `/help`    | Show welcome banner and help |
| `/context` | Inspect the raw messages array (the actual context window) |
| `/stats`   | Show cumulative token statistics |
| `/clear`   | Reset conversation and token counts |
| `/docs`    | List available knowledge base documents |
| `/quit`    | Exit the demo |

## Key Concepts Demonstrated

| Concept | Where to Look |
|---------|---------------|
| Writing context (system prompt) | `agent.py` → `SYSTEM_PROMPT` |
| Messages array = context window | `agent.py` → `self.messages` |
| Agent loop (tool use cycle) | `agent.py` → `run_turn()` while loop |
| Token counting (real costs) | `agent.py` → `response.usage` |
| Tool results entering context | `agent.py` → `tool_result` append |
| Tool definitions as fixed cost | `tools.py` → `get_tool_definitions()` |
| Selecting context (retrieval) | `retrieval.py` → `KnowledgeBase.search()` |
| Framework vs manual tradeoff | Compare `agent.py` (hand-rolled loop, ~245 lines) vs `../full_agent_app.py` (claude-agent-sdk version over the same `knowledge_base/`, ~184 lines) |

## File Overview

```
├── app.py                    # Entry point: TUI + slash commands
├── agent.py                  # Agent loop with manual context management (CORE)
├── retrieval.py              # TF-IDF document search
├── tools.py                  # Tool schemas (Anthropic API format) + dispatch
├── display.py                # ANSI terminal output helpers
├── knowledge_base/           # 6 markdown docs on course topics
│   ├── context-windows.md
│   ├── prompt-vs-context-eng.md
│   ├── agentic-systems.md
│   ├── rag-patterns.md
│   ├── context-failures.md
│   └── manus-architecture.md
└── README.md                 # This file
```
