> **TL;DR** — 5 sessions, 4 runnable demos.
> `export ANTHROPIC_API_KEY=… && cd demos/<name> && uv run app.py`

# Context Engineering Hands-On

**O'Reilly Live Training** — Teaching developers how to design, manage, and optimize the context that flows into LLMs and agentic systems.

Five sessions across ~4.5 hours: slides, live demos, and hands-on code — all runnable with [uv](https://docs.astral.sh/uv/) and an Anthropic API key.

---

## Course Structure

| Session | Topic | Demo |
|---------|-------|------|
| 1 | Introduction to Context Engineering | Taught live — no committed demo |
| 2 | Engineering Context in Agentic Systems | Hand-rolled agent loop with TF-IDF retrieval |
| 2 / 4 | Context Engineering in Modern AI Apps | FastAPI chat app with structured artifact output |
| 3 | Diagnosing and Fixing Context Failures | Taught live — no committed demo |
| 5 | Tools and Techniques for Modern Development | Taught live in Claude Code — no committed demo directory |
| Bonus | Agentic RAG via the Agent SDK | `full_agent_app.py` — custom MCP tools over the knowledge base |
| Bonus | Context Engineering Chat Agent Overview | From-scratch tool-use agent loop, quiz app, structured-output primer |

---

## Prerequisites

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** — the package manager used by every demo
- **Anthropic API key** — get one at [console.anthropic.com](https://console.anthropic.com)

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Set your API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Add it to your shell profile (`~/.zshrc` or `~/.bashrc`) to persist it across sessions. Alternatively, create a `.env` file in any demo directory:

```bash
echo "ANTHROPIC_API_KEY=sk-ant-..." > demos/<demo-name>/.env
```

### Clone the repo

```bash
git clone <REPO_URL>
cd context-engineering-hands-on
```

No global `pip install` or virtual environment needed — every demo uses `uv run` to manage its own dependencies inline.

---

## Demos

### Session 2 — Agentic Document Retrieval

**Directory:** `demos/agentic-retrieval/`

A hand-rolled agent loop with explicit context management and TF-IDF document retrieval. Every context engineering decision is visible — no framework magic.

**Run:**

```bash
cd demos/agentic-retrieval
uv run app.py
```

**Suggested query sequence** (follow this order to watch context grow):

1. `What documents do you have?` — triggers `list_documents`
2. `What is context engineering?` — triggers `search_documents`
3. `Tell me more about the Manus architecture` — triggers `get_document` for full content
4. `How does RAG relate to what Manus does?` — multi-doc synthesis
5. `/context` — inspect the raw messages array
6. `/stats` — see cumulative token counts
7. `Summarize everything we've discussed` — large input context, high cost
8. `/clear` — reset and compare fresh vs. accumulated cost

**Slash commands:**

| Command | Description |
|---------|-------------|
| `/context` | Inspect the raw messages array |
| `/stats` | Show cumulative token statistics |
| `/clear` | Reset conversation and token counts |
| `/docs` | List knowledge base documents |
| `/help` | Show help |
| `/quit` | Exit |

---

### Session 2 / 4 — Chat with Artifacts

**Directory:** `demos/chat-with-artifacts/`

A FastAPI backend + single-file frontend demonstrating a 3-layer system prompt, structured tool output, and a growing artifact registry injected into context.

**Run:**

```bash
cd demos/chat-with-artifacts
uv run app.py
```

Then open **http://127.0.0.1:8000** in your browser.

**What to try:**
- Ask about any topic to see the artifact system in action
- Watch the token counter grow in the stats bar as artifacts are created
- Ask to be quizzed to see context from earlier turns referenced in new outputs

**What's demonstrated:**
- 3-layer system prompt (persona + artifact schemas + dynamic session state)
- Structured output via a single `create_artifact` tool
- Dynamic context injection — the artifact registry grows and re-enters the system prompt
- Conversation history as accumulating context

**Bonus — minimal structured-outputs primer:** `structured_outputs_demo.py` in the same directory is a standalone ~30-second read showing the same prompt forced through 3 different tool schemas (no FastAPI scaffolding). Run with `uv run structured_outputs_demo.py`.

---

### Agentic RAG via the Agent SDK

**Directory:** `demos/full_agent_app.py` (single script; uses `demos/agentic-retrieval/knowledge_base/` by default)

A simplified agentic-RAG CLI built on `claude-agent-sdk` instead of a hand-rolled loop — a framework-assisted counterpoint to the Session 2 demo above.

**Run:**

```bash
uv run demos/full_agent_app.py
# or point it at a different folder of .md files
uv run demos/full_agent_app.py path/to/folder
```

**What's demonstrated:**
- Three custom MCP tools (`list_docs`, `read_doc`, `search_docs`) registered via `create_sdk_mcp_server` and exposed to Claude through `ClaudeAgentOptions`
- Claude decides when to search vs. read a full file, guided by a "search first, then read the top 1-2 files" instruction in the system prompt
- Framework vs. manual tradeoff — contrast the ~185 lines here with `agentic-retrieval/agent.py`
- Uses `claude-sonnet-5`

---

### Context Engineering Chat Agent Overview

**Directory:** `demos/live-demo-chat-agent-ctx-eng-overview/`

**Files:**
- `chat.py` — a from-scratch tool-use agent loop (no framework) with `create_file`, `read_file`, `search_files` tools plus Claude's built-in web search
- `quiz_app.py` — a small FastAPI chat-driven quiz generator using structured output (`messages.parse`)
- `structured_output_example.py` — a minimal ~30-line primer for `messages.parse`
- `company_job_openings.txt`, `lucas-rocks-in-live-sessions.txt` — grounding fixtures read by `chat.py`'s tools to show grounding vs. parametric recall

**Run:**

```bash
uv run demos/live-demo-chat-agent-ctx-eng-overview/chat.py
uv run demos/live-demo-chat-agent-ctx-eng-overview/quiz_app.py   # then open http://127.0.0.1:8501
uv run demos/live-demo-chat-agent-ctx-eng-overview/structured_output_example.py
```

**What's demonstrated:**
- Explicit context window management in a hand-rolled agent loop (`Agent.messages`)
- A tool-use cycle built from scratch: `create_file` / `read_file` / `search_files` + built-in web search
- Grounding vs. memory — reading the fixture `.txt` files beats parametric recall
- Structured output via `messages.parse`, from a minimal primer to a full quiz app with a browser UI
- Uses `claude-sonnet-5`

---

### Session 5 — Tools and Techniques

Taught live in Claude Code during the session — no committed demo directory. Covers advanced context engineering tools and patterns for production systems using Claude Code itself as the demo environment.

---

## Repo Structure

```
context-engineering-hands-on/
├── presentation-slides/                   # Slide decks (.html — remark.js live + handout)
├── assets/                                # Reference PDFs (attention paper, cheatsheets)
└── demos/
    ├── agentic-retrieval/                       # Session 2 — hand-rolled agent loop
    │   ├── app.py                               # Entry point (TUI + slash commands)
    │   ├── agent.py                             # Agent loop — THE core teaching file
    │   ├── retrieval.py                         # TF-IDF document search
    │   ├── tools.py                             # Tool schemas + dispatch
    │   ├── display.py                           # ANSI terminal output
    │   └── knowledge_base/                      # 6 markdown docs on course topics
    ├── chat-with-artifacts/                     # Session 2/4 — FastAPI app
    │   ├── app.py                               # FastAPI backend
    │   ├── schemas.py                           # Artifact type schemas
    │   ├── structured_outputs_demo.py           # Bonus: minimal structured-outputs primer
    │   └── static/index.html                    # Single-file frontend
    ├── full_agent_app.py                        # Agentic RAG via claude-agent-sdk MCP tools
    └── live-demo-chat-agent-ctx-eng-overview/    # From-scratch chat agent + quiz app + structured-output primer
        ├── chat.py                               # From-scratch tool-use agent loop
        ├── quiz_app.py                           # FastAPI chat-driven quiz generator
        ├── structured_output_example.py          # Minimal messages.parse primer
        ├── company_job_openings.txt              # Grounding fixture
        └── lucas-rocks-in-live-sessions.txt       # Grounding fixture
```

---

## Troubleshooting

**`ANTHROPIC_API_KEY` not found**

```bash
# Check if it's set
echo $ANTHROPIC_API_KEY

# Set it for the current session
export ANTHROPIC_API_KEY=sk-ant-...
```

**`uv: command not found`**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Then restart your terminal
```

**Port 8000 already in use (chat-with-artifacts)**

```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9
# Then re-run
uv run app.py
```

---

*Course slides and reference materials are in `presentation-slides/` and `assets/`.*
