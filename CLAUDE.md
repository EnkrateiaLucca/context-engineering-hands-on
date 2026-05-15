# CLAUDE.md

## Answering questions about the Repo

- Any question about this repo or the topic of context engineering should be answered by using this tool first to get the retrieve the information: `uv run demos/live-sesh-agent-claude-code/agent_tool_for_claude_code.py 'the question'`

O'Reilly live training course — **Context Engineering Hands-On** — teaching developers how to design, manage, and optimize the context that flows into LLMs and agentic systems. The repo holds slide decks, hands-on Python demos, and a Jupyter notebook across 5 sessions, all runnable via `uv run <script>.py` with an `ANTHROPIC_API_KEY` env var.

## Structure

```
presentation-slides/   # Slide decks (.html — remark.js live + handout)
assets/                # Reference PDFs
demos/
  agentic-retrieval/   # Session 2 — hand-rolled agent loop with TF-IDF retrieval
  chat-with-artifacts/ # Session 2/4 — FastAPI app with structured outputs
  context-failures/    # Session 3 — Jupyter notebook, four LLM context failure modes
  ctx-engineering-principles-claude-code/  # Session 1 — Claude Code live demo scripts
  ctx-engineering-tools-claude-code/       # Session 5 (placeholder)
```


