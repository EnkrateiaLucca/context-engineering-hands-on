# CLAUDE.md

O'Reilly live training course — **Context Engineering Hands-On** — teaching developers how to design, manage, and optimize the context that flows into LLMs and agentic systems. The repo holds slide decks and hands-on Python demos across 5 sessions, all runnable via `uv run <script>.py` with an `ANTHROPIC_API_KEY` env var.

## Structure

```
presentation-slides/   # Slide decks (.html — remark.js live + handout)
assets/                # Reference PDFs
demos/
  agentic-retrieval/                       # Session 2 — hand-rolled agent loop with TF-IDF retrieval
  chat-with-artifacts/                     # Session 2/4 — FastAPI app with structured outputs
  full_agent_app.py                        # Agentic RAG via claude-agent-sdk custom MCP tools
  live-demo-chat-agent-ctx-eng-overview/   # From-scratch tool-use agent loop, quiz app, structured-output primer
```


