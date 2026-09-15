# Scheduled Agents — Cron Jobs for Claude Code

Session 5 material on **tools and techniques for modern development**: putting an
agent on a schedule so it does useful work while you sleep.

The idea is simple — a cron entry runs a headless Claude Code agent
(`claude -p "<prompt>"` with the tools it needs), the agent does the work, and it
posts the result somewhere you'll see it (Discord, a file, your Obsidian vault, a
git branch). Context engineering is what makes these reliable: each job gets a
tight prompt, only the tools it needs, and a fresh context window every run.

---

## Example use-cases

Real-world examples of what a scheduled agent can do. Each is one cron-driven
Claude Code run.

| Use-case | What it does |
|----------|--------------|
| **Daily news / AI digest** | Top stories summarized to Discord |
| **Standup Prep** | Reviews git log, drafts yesterday / today / blockers |
| **Friday Wind-down** | Checks todos, issues, messages for the weekend |
| **Nightly Project Backup** | Archives and confirms backup completion |
| **Weekly Dependency Audit** | Flags outdated packages every Sunday |
| **Nightly Health Check** | Pings API, memory, model availability — confirms all jobs ran properly |
| **Apple Notes → Obsidian** | Summarises notes, compiles into vault |

---

## How it works

Each use-case is a **cron-driven headless Claude run** that posts its output to a
destination (Discord webhook, a file, the vault, or a PR).

```cron
# Daily news / AI digest — 8am, summarize + post to Discord
0 8 * * *   claude -p "Summarize today's top AI stories and post to Discord" --allowedTools "WebSearch,Bash"

# Standup Prep — weekday mornings, read git log, draft standup notes
30 8 * * 1-5   claude -p "Review the git log since yesterday and draft my standup: yesterday / today / blockers"

# Weekly Dependency Audit — every Sunday
0 9 * * 0   claude -p "Audit dependencies in this repo and flag anything outdated"
```

**Why context engineering matters here:** an unattended agent has no human to
correct a bloated or poisoned context mid-run. The reliability of these jobs comes
from the same principles taught in the earlier sessions —

- **Tool loadout** — give each job only the tools it needs (`--allowedTools`), not the whole toolbox.
- **Fresh context per run** — every cron invocation starts clean; no accumulated cruft across days.
- **Grounding over memory** — have the agent `Read` the git log / package file / notes rather than recall them.
- **Structured hand-off** — the job's last step is a well-formed post (Discord message, JSON, a vault note), not a chat transcript.

---

*Placeholder demo scripts for these jobs land here as Session 5 develops. For now
this file is the reference for the cron use-cases shown in the slides.*
