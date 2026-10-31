> **TL;DR** — 5 sessions, 10 runnable demos.
> `cp .env.example .env` (add your key), then run each demo with the **Run:** command in its section below.

# Context Engineering Hands-On

**O'Reilly Live Training** — Teaching developers how to design, manage, and optimize the context that flows into LLMs and agentic systems.

Five sessions across ~4.5 hours: slides, live demos, and hands-on code — all runnable with [uv](https://docs.astral.sh/uv/) and an Anthropic API key.

---

## Course Structure

| Session | Topic | Demo |
|---------|-------|------|
| 1 | Introduction to Context Engineering | `demos/live-ctx-intro-demo/` — what the model sees, context budget, the four moves, agent-loop growth |
| 2 | Engineering Context in Agentic Systems | Hand-rolled agent loop with TF-IDF retrieval; live-coded agent loops (`live_simple_agent.py`, shell-tool retrieval agents) |
| 2 / 4 | Context Engineering in Modern AI Apps | FastAPI chat app with structured artifact output |
| 3 | Diagnosing and Fixing Context Failures | Taught live — no committed demo |
| 4 | Context Engineering Patterns in Modern AI Apps | Agent Skills — a `.pptx` deck built from data (prepared + live-coded) |
| 5 | Tools and Techniques for Modern Development | Claude Code primitives (CLAUDE.md, slash commands, hooks, sub-agents, MCP) + scheduled agents on cron |
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

Add it to your shell profile (`~/.zshrc` or `~/.bashrc`) to persist it across sessions. Alternatively, copy the template to a `.env` file at the repo root and put your key in it — every demo loads it with `python-dotenv`:

```bash
cp .env.example .env   # then edit ANTHROPIC_API_KEY in .env
```

### Clone the repo

```bash
git clone <REPO_URL>
cd context-engineering-hands-on
```

No global `pip install` or virtual environment needed — every demo uses `uv run` to manage its own dependencies inline.

---

## Demos

### Session 1 — Context Engineering Basics

**Directory:** `demos/live-ctx-intro-demo/`

A ten-slide primer (`slides/intro-context-engineering.html`) plus four short scripts, one per idea. The scripts open `../assets/` relative to `code/`, so run them from there.

**Run:**

```bash
cd demos/live-ctx-intro-demo/code
uv run 01_what_the_model_sees.py   # the "prompt" is one flat token list built from slots
uv run 02_context_budget.py        # needle-in-a-haystack: tokens, latency, accuracy vs. filler
uv run 03_four_moves.py            # Write / Select / Compress / Isolate, minimal versions
uv run 04_agent_loop_growth.py     # per-turn token growth in a tool loop, raw vs. trimmed
```

**What's demonstrated:**
- Same question, different context, different answer — the model only sees what you assemble
- The context window as a budget: filler costs tokens and latency, and can cost accuracy
- The four moves in their smallest honest form
- Context that accumulates turn by turn in an agent loop, and what trimming tool results saves

---

### Session 2 — Simplest Agent Loop (live-coded)

**Directory:** `demos/live_simple_agent.py` (single script)

The smallest possible agent: one `calculator` tool and a loop that keeps calling the model until it stops asking for tools. Every request and tool result is appended to `messages` — the context the model sees next turn.

**Run:**

```bash
uv run demos/live_simple_agent.py
```

**What's demonstrated:**
- Agent = LLM + tools in a loop, in under 90 lines
- `stop_reason == "tool_use"` as the loop condition
- Tool results flowing back into context as `tool_result` blocks
- Uses `claude-sonnet-5-5`

---

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

### Session 2 — Shell-Tool Retrieval Agents (live-coded)

**Directories:** `demos/live-agent-retrieval/` and `demos/live-agent-retrieval-plus-write-select-compress-isolate/`

An `Agent` class that answers questions about files using three shell-backed tools — `find_files` (`find`), `read_file` (`sed -n`) and `grep_files` (`grep -rn`) — sandboxed to one working directory. The second folder is the same agent plus a `write_file` tool, so it can save its answers to disk, and a small terminal chat around it. Despite the folder name, only the *write* move is implemented; select, compress and isolate are not in the code.

**Run:**

```bash
# bare retrieval agent — one scripted turn: summarize the Python files in this folder
cd demos/live-agent-retrieval
uv run agent.py

# with write_file — scripted two turns: summarize, then write the summary to a markdown file
cd ../live-agent-retrieval-plus-write-select-compress-isolate
uv run agent.py
# or chat with it (/help, /files, /clear, /history, /quit; @path inlines a file)
uv run app.py
```

Files the agent writes land in that folder; delete them after the demo.

**What's demonstrated:**
- Retrieval as tool use — the agent discovers, greps and reads files on demand instead of being handed them
- Tool descriptions shaping agent behaviour (custom schemas instead of the built-in bash tool)
- Path sandboxing: model-supplied paths are untrusted and resolved against a fixed root
- *Write* — persisting output outside the context window
- Uses `claude-sonnet-5-5`

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

### Session 4 — Agent Skills: a Deck from Data

**Directories:** `demos/agents-with-skills/` (prepared) and `demos/live-agents-with-skills/` (live-coded)

Claude turns a sales CSV and a `notes.md` of presenter instructions into a `.pptx` deck. Instead of stuffing python-pptx instructions into the prompt, the script attaches Anthropic's managed `pptx` skill to the code-execution container: Claude loads the skill's instructions only when it needs them, builds the deck in the sandbox, and the script downloads the file into `output/`.

**Run:**

```bash
uv run demos/agents-with-skills/pptx_from_data_agent.py            # generates synthetic data, builds the deck
uv run demos/agents-with-skills/pptx_from_data_agent.py --no-gen   # reuse the existing data/ folder
uv run demos/live-agents-with-skills/ppt_agent.py                  # live-coded version, uses its data/ folder
```

**What's demonstrated:**
- Skills as context loaded on demand rather than up front
- Files API uploads (`container_upload`) + the `code_execution` tool
- Downloading generated files by `file_id`
- Uses `claude-opus-5-5`

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
- Uses `claude-sonnet-5-5`

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
- Uses `claude-sonnet-5-5`

---

### Session 5 — Tools and Techniques: Claude Code Primitives + Scheduled Agents

**Directory:** `demos/ctx-engineering-tools-claude-code/` (scheduled-agents material)

The session covers the Claude Code primitives that make context engineering tractable — CLAUDE.md, custom slash commands, hooks, sub-agents and MCP — taught live from the slides, then closes on scheduled agents: putting an agent on a **cron schedule** so it does useful work unattended — a headless `claude -p` run that posts its output to Discord, a file, or your vault. See `README.md` in that directory for the full set of example use-cases (daily AI digest, standup prep, dependency audit, nightly health check, Apple Notes → Obsidian, and more) and why context engineering is what makes unattended runs reliable.

---

## Repo Structure

```
context-engineering-hands-on/
├── index.html                             # Course landing page
├── .env.example                           # Copy to .env and add ANTHROPIC_API_KEY
├── requirements/                          # requirements.in + compiled requirements.txt (optional shared venv)
├── presentation-slides/                   # Slide decks (.html — remark.js live + handout)
├── assets/                                # Reference PDFs (attention paper, cheatsheets)
└── demos/
    ├── live-ctx-intro-demo/                     # Session 1 — context engineering basics
    │   ├── slides/intro-context-engineering.html # Ten-slide primer (remark.js)
    │   ├── code/                                # 01–04 demo scripts + _common.py (run from here)
    │   └── assets/                              # Knowledge base + reading notes used by the scripts
    ├── live_simple_agent.py                     # Session 2 — simplest agent loop (calculator tool)
    ├── agentic-retrieval/                       # Session 2 — hand-rolled agent loop
    │   ├── app.py                               # Entry point (TUI + slash commands)
    │   ├── agent.py                             # Agent loop — THE core teaching file
    │   ├── retrieval.py                         # TF-IDF document search
    │   ├── tools.py                             # Tool schemas + dispatch
    │   ├── display.py                           # ANSI terminal output
    │   └── knowledge_base/                      # 6 markdown docs on course topics
    ├── live-agent-retrieval/                    # Session 2 — shell-tool retrieval agent (live-coded)
    │   ├── agent.py                             # Agent loop; runs one scripted turn
    │   └── tools.py                             # find_files / read_file / grep_files
    ├── live-agent-retrieval-plus-write-select-compress-isolate/  # Same agent + write_file (write only)
    │   ├── agent.py                             # Agent loop; runs two scripted turns
    │   ├── app.py                               # Terminal chat around Agent
    │   └── tools.py                             # Shell tools + write_file
    ├── chat-with-artifacts/                     # Session 2/4 — FastAPI app
    │   ├── app.py                               # FastAPI backend
    │   ├── schemas.py                           # Artifact type schemas
    │   ├── structured_outputs_demo.py           # Bonus: minimal structured-outputs primer
    │   └── static/index.html                    # Single-file frontend
    ├── agents-with-skills/                      # Session 4 — pptx from data via Agent Skills (prepared)
    │   ├── pptx_from_data_agent.py              # Generates data, builds the deck
    │   └── data/                                # sales_2025.csv + notes.md
    ├── live-agents-with-skills/                 # Session 4 — same idea, live-coded
    │   ├── ppt_agent.py                         # Builds the deck from data/
    │   ├── data/                                # sales_2025.csv + notes.md
    │   └── output/                              # Deck produced on teaching day
    ├── ctx-engineering-tools-claude-code/       # Session 5 — scheduled agents (Claude Code on cron)
    │   └── README.md                            # Use-cases, cron entries, why context engineering matters
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
