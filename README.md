> **TL;DR** — 5 sessions, 4 runnable demos, 1 notebook.
> `export ANTHROPIC_API_KEY=… && cd demos/<name> && uv run app.py`

# Context Engineering Hands-On

**O'Reilly Live Training** — Teaching developers how to design, manage, and optimize the context that flows into LLMs and agentic systems.

Five sessions across ~4.5 hours: slides, live demos, and hands-on code — all runnable with [uv](https://docs.astral.sh/uv/) and an Anthropic API key.

---

## Course Structure

| Session | Topic | Demo |
|---------|-------|------|
| 1 | Introduction to Context Engineering | Claude Code live demo scripts |
| 2 | Engineering Context in Agentic Systems | Hand-rolled agent loop with TF-IDF retrieval |
| 2 / 4 | Context Engineering in Modern AI Apps | FastAPI chat app with structured artifact output |
| 3 | Diagnosing and Fixing Context Failures | Jupyter notebook — four failure modes |
| 5 | Tools and Techniques for Modern Development | Claude Code primitives demo — CLAUDE.md, slash command, hook, MCP |

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

### Session 1 — Claude Code Live Demos

**Directory:** `demos/ctx-engineering-principles-claude-code/`

This is a **live instructor demo** — no Python script to run. Follow the guide in your terminal using Claude Code.

**Files:**
- `live-demo-guide.md` — Step-by-step demo script (5 demos, ~30 min)
- `context-window-guide.md` — Supporting reference: context window mechanics
- `long-doc-middle.txt` / `long-doc-top.txt` — Documents used in the "Lost in the Middle" demo

**Prerequisites:**

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Verify it works
claude -p "hello"
```

**Running the demo:**

Open `live-demo-guide.md` and follow the instructions. Each demo section tells you exactly what to type in the Claude Code terminal, what to expect, and what to highlight for the audience.

**What's demonstrated:**
- Demo 1: What's already in the context window before you type anything
- Demo 2: Context rot — how accumulated irrelevant context degrades output quality
- Demo 3: Lost in the Middle — how information position affects retrieval
- Demo 4: Grounding vs. memory — why `Read <file>` beats parametric recall
- Demo 5: All 7 Playbook rules in rapid succession

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

### Session 3 — Context Failures Notebook

**Directory:** `demos/context-failures/`

A Jupyter notebook walking through all four LLM context failure modes: Poisoning, Distraction, Confusion, and Clash. Each section runs a **broken** version, then a **fixed** version, and compares token costs side by side.

#### Kernel Setup (required before first run)

The notebook uses `anthropic` and `IPython.display` — you need a Jupyter kernel that has these installed.

**Option A — Install into an existing kernel (quickest):**

```bash
cd demos/context-failures
pip install anthropic ipython jupyter
```

If you already have Jupyter installed system-wide, this is enough. Open the notebook and select your default kernel.

**Option B — Dedicated uv environment (recommended for isolation):**

```bash
cd demos/context-failures

# Create a virtual environment and install dependencies
uv venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
uv pip install anthropic ipython jupyter ipykernel

# Register it as a named Jupyter kernel
python -m ipykernel install --user --name context-failures --display-name "Context Failures (uv)"
```

Then launch Jupyter:

```bash
jupyter notebook context_failures.ipynb
# or
jupyter lab
```

When the notebook opens, select **"Context Failures (uv)"** from the kernel picker (top-right or Kernel menu).

**Option C — VS Code / Cursor:**

Open `context_failures.ipynb` in VS Code/Cursor. When prompted to select a kernel, choose the `.venv` interpreter at `demos/context-failures/.venv/bin/python`. VS Code will detect it automatically if you created the venv inside the demo directory.

#### API Key Setup

The notebook reads `ANTHROPIC_API_KEY` from the environment. Set it before launching Jupyter:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
jupyter notebook context_failures.ipynb
```

Or create a `.env` file in the demo directory — the notebook's setup cell will pick it up if you add a `load_dotenv()` call, or just export it in the shell that launches Jupyter.

**Verify the key is visible:**

```python
# Run this in a notebook cell to confirm
import os
print(os.environ.get("ANTHROPIC_API_KEY", "NOT SET"))
```

#### Running the Notebook

Run cells **top to bottom** — the `results` dict accumulates outputs used in the final dashboard. Don't skip the setup cell (Section 0).

**What's covered:**

| Section | Failure Mode | What Goes Wrong | Fix Applied |
|---------|-------------|-----------------|-------------|
| 1 | Poisoning | Hallucinated assistant message overrides system prompt | Context pruning + validation instruction |
| 2 | Distraction | Prior brute-force examples bias model away from DP solution | Context quarantine + summarization |
| 3 | Confusion | 12 irrelevant tool schemas overwhelm a simple factual question | Tool loadout (remove unused tools) |
| 4 | Clash | Budget and luxury travel plans coexist, producing incoherent output | Pruning + state replacement |
| 5 | Dashboard | Side-by-side token comparison for all four failures | — |

Each failure cell is self-contained — you can run them independently if you only want to demonstrate one.

---

### Session 5 — Context Engineering Tools in Claude Code

**Directory:** `demos/ctx-engineering-tools-claude-code/`

A ~20-minute **live instructor demo** showing four Claude Code primitives co-located in one project — no Python script to run, no `npm install` or Docker (`uv`/`uvx` only). Open the project in Claude Code and walk through each primitive.

**Files:**
- `CLAUDE.md` — Minimal repo-level context file (carries only what the agent can't infer)
- `.claude/commands/audit-context.md` — Custom `/audit-context` slash command that wraps the course's retrieval helper
- `.claude/settings.json` — `PostToolUse` hook that offloads Bash/Read tool outputs to `.claude/tool-outputs/`
- `.mcp.json` — One `fetch` MCP server registered for live HTTP retrieval

**Suggested flow (~20 min):**
1. Open `CLAUDE.md` — note how short it is; a bloated context file makes the agent worse, so this one carries only what it can't infer.
2. Run `/audit-context "where does Session 3 cover context failures?"` — a slash command is just a markdown file with frontmatter, no plugin install.
3. Trigger any Bash or Read tool call (e.g. `ls demos/`), then open `.claude/tool-outputs/` to show the new file — the "offload large outputs from the live window" pattern.
4. Use the `fetch` MCP server to retrieve a short doc page; inspect `.mcp.json` and explain stdio vs. http transport.

**What's demonstrated:**
- CLAUDE.md as a deliberately minimal, high-signal context file
- Slash commands as zero-install, file-based agent shortcuts
- Hooks for offloading large tool outputs out of the live context window
- MCP servers for extending an agent with live external retrieval

---

## Repo Structure

```
context-engineering-hands-on/
├── presentation-slides/                   # Slide decks (.html — remark.js live + handout)
├── assets/                                # Reference PDFs (attention paper, cheatsheets)
└── demos/
    ├── ctx-engineering-principles-claude-code/  # Session 1 — Claude Code live demo guide
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
    │   └── static/index.html                    # Single-file frontend
    ├── context-failures/                        # Session 3 — Jupyter notebook
    │   └── context_failures.ipynb               # Four failure modes, broken + fixed
    ├── live-sesh-agent-claude-code/             # Retrieval helper for CLAUDE.md + /audit-context
    │   └── agent_tool_for_claude_code.py        # Answers repo questions via TF-IDF retrieval
    └── ctx-engineering-tools-claude-code/       # Session 5 — Claude Code primitives demo
        ├── CLAUDE.md                            # Minimal repo-level context file
        ├── .claude/commands/audit-context.md    # /audit-context slash command
        ├── .claude/settings.json                # PostToolUse hook (offloads tool outputs)
        └── .mcp.json                            # fetch MCP server
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

**Jupyter kernel not finding the API key**

Jupyter inherits environment variables from the shell that launched it. Always `export ANTHROPIC_API_KEY=...` *before* running `jupyter notebook`, not after.

**`ModuleNotFoundError: No module named 'anthropic'` in the notebook**

Your selected kernel doesn't have the package installed. Either install it into the active kernel (`pip install anthropic`) or switch to the kernel you created with `ipykernel install` (see Option B above).

**Port 8000 already in use (chat-with-artifacts)**

```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9
# Then re-run
uv run app.py
```

---

*Course slides and reference materials are in `presentation-slides/` and `assets/`.*
