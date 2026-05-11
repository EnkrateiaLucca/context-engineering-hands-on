# Session 5 Demo — Context Engineering Tools in Claude Code

A ~20-minute live demo showing four Claude Code primitives co-located in one project:

| File | Primitive |
|---|---|
| `CLAUDE.md` | Minimal repo-level context file (per ETH Zurich AGENTS.md finding, Feb 2026) |
| `.claude/commands/audit-context.md` | Custom slash command that wraps the course's retrieval helper |
| `.claude/settings.json` | `PostToolUse` hook that offloads tool outputs to `.claude/tool-outputs/` |
| `.mcp.json` | One MCP server (`fetch`) registered for live HTTP retrieval |

## Suggested live flow (20 min)

1. **(2 min) Open `CLAUDE.md`.** Read it out loud — note how short it is. Reference the ETH Zurich result: most CLAUDE.md files make agents *worse*; this one only carries what the agent can't infer.
2. **(5 min) Run `/audit-context "where does Session 3 cover context failures?"`** inside Claude Code. Show how a slash command is just a markdown file with frontmatter — no plugin install.
3. **(7 min) Trigger any Bash or Read tool call** (e.g. `ls demos/`). Then open `.claude/tool-outputs/` and show the new file. This is the "offload large outputs from the live window" pattern. Discuss when you'd want this on vs. off.
4. **(6 min) Use the `fetch` MCP server.** Ask Claude to fetch a short doc page (e.g. the Claude Code hooks reference). Inspect `.mcp.json` and explain stdio vs. http transport.

## Where this fits in the deck

See `presentation/context-engineering-hands-on.html` — Session 5 (slide deck not yet authored; the slides-editor sub-agent owns that artifact next).

## Constraints honored

- No npm install, no docker.
- `uv` and `uvx` only (already in the course environment).
- Total project surface area is under ~150 lines so it stays live-codable.
