# CLAUDE.md

O'Reilly live training course — **Context Engineering Hands-On** — teaching developers how to design, manage, and optimize the context that flows into LLMs and agentic systems. The repo holds slide decks and hands-on Python demos across 5 sessions, all runnable via `uv run <script>.py` with an `ANTHROPIC_API_KEY` env var.

## Structure

```
presentation-slides/   # Slide deck (.html — remark.js) + PDF export
assets/                # Reference PDFs
demos/
  live-ctx-intro-demo/                     # Session 1 — intro primer slides + 4 scripts (run from code/)
  live_simple_agent.py                     # Session 2 — simplest agent loop, one calculator tool
  agentic-retrieval/                       # Session 2 — hand-rolled agent loop with TF-IDF retrieval
  live-agent-retrieval/                    # Session 2 — live-coded shell-tool retrieval agent (find/sed/grep)
  live-agent-retrieval-plus-write-select-compress-isolate/  # Same agent + write_file tool (implements write only)
  chat-with-artifacts/                     # Session 2/4 — FastAPI app with structured outputs
  agents-with-skills/                      # Session 4 — pptx from data via the Agent Skills pptx skill (prepared)
  live-agents-with-skills/                 # Session 4 — same pptx-from-data agent, live-coded
  ctx-engineering-tools-claude-code/       # Session 5 — scheduled agents: Claude Code on a cron (README only)
  full_agent_app.py                        # Agentic RAG via claude-agent-sdk custom MCP tools
  live-demo-chat-agent-ctx-eng-overview/   # From-scratch tool-use agent loop, quiz app, structured-output primer
```


