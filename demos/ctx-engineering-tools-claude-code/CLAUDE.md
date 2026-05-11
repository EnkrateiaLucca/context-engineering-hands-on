<!-- Session 5 demo — kept deliberately small. ETH Zurich's AGENTS.md study (Feb 2026, arXiv 2602.11988) found long context files degrade agent performance; aim for <200 words, human-written, only what the agent can't infer from the repo itself. -->

# ctx-engineering-tools-claude-code

A tiny live demo for Session 5 of *Context Engineering Hands-On*. It shows four Claude Code primitives co-located in one project: this CLAUDE.md, a custom slash command, a PostToolUse hook, and an MCP server.

## How to answer questions about this repo

Use the course retrieval helper rather than free-form grepping:

```
uv run ../live-sesh-agent-claude-code/agent_tool_for_claude_code.py "your question"
```

The `/audit-context` slash command wraps that call.

## Non-obvious behavior

The PostToolUse hook in `.claude/settings.json` writes every Bash and Read tool result to `.claude/tool-outputs/`. That directory is git-ignored locally during the demo — students inspect it live to see the "offload large tool outputs out of the context window" pattern in action.
