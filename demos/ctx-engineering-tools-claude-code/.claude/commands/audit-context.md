---
description: Ask the course retrieval helper a question about this repo
argument-hint: <question in quotes>
allowed-tools: Bash(uv run *)
---

Run the course's repo-aware retrieval agent to answer the user's question. Execute exactly this command and return its output verbatim, with no additional commentary:

```
uv run ../live-sesh-agent-claude-code/agent_tool_for_claude_code.py "$ARGUMENTS"
```

The helper lives at `demos/live-sesh-agent-claude-code/agent_tool_for_claude_code.py` (relative path above assumes you're running from `demos/ctx-engineering-tools-claude-code/`). It takes a single quoted question, runs an internal Claude agent loop with Read/Glob/Grep over the repo, and prints the result.
