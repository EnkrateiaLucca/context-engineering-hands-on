# `/context` Token Deltas for Demo 1

## Context

`demos/ctx-engineering-principles-claude-code/live-demo-guide.md` (Demo 1, "Context Is Everything", ~5 min) uses three `/context` invocations to make the invisible visible: the size of the context window before any user input, after a trivial question, and after a file read. The course briefing (`IMPROVEMENTS.md` §4.1) asks for `EXPECTED DELTA: ~X tokens` annotations on each invocation so the instructor doesn't have to squint at the projector mid-demo.

These numbers cannot be measured statically — `/context` is a built-in Claude Code slash command that introspects the current session's live token usage [source: https://code.claude.com/docs/en/how-claude-code-works]. They depend on Claude Code version, the user's `CLAUDE.md`, installed MCP servers, and which tool definitions ship with the current build. So the values below are **reasoned estimates**, all explicitly `[unverified]`.

## Findings

### Invocation 1 — Fresh session baseline (live-demo-guide.md L48-52)

Right after `claude` launch, before any user message.

What's loaded:
- Claude Code system prompt — ~3-4k tokens [unverified, but consistent with reverse-engineering work at https://github.com/Piebald-AI/claude-code-system-prompts]
- Built-in tool definitions (Read/Edit/Write/Bash/Grep/Glob/WebFetch/WebSearch/etc., ~24 tools per the same reverse-engineering source) — ~8-12k tokens [unverified]
- This repo's `CLAUDE.md` (currently ~14 lines including the agent-tool instruction) — ~150 tokens [unverified]
- No conversation history yet — 0 tokens

**EXPECTED DELTA on first `/context`: shows ~12-18k tokens already used (out of 200k window).** [unverified]

Pedagogical hook: "You haven't typed anything yet and ~7-9% of the window is already gone."

### Invocation 2 — After "What is the capital of Portugal?" (live-demo-guide.md L66-68)

Increment is the user message + Claude's short answer + any internal reasoning tokens emitted (Claude Code tracks both).

- User message: ~10 tokens
- Assistant response (1-2 sentences): ~30-60 tokens
- Internal reasoning (Opus 4.x emits reasoning blocks even on trivial queries): ~50-200 tokens [unverified]

**EXPECTED DELTA from invocation 1: +100-300 tokens (round to ~200).** [unverified]

Pedagogical hook: "Trivial exchange, trivial delta. The interesting jumps come from tools and reads."

### Invocation 3 — After `Read demos/.../context-window-guide.md` (live-demo-guide.md L80-82)

The guide itself states "The entire file (~3,000 tokens) is now sitting in the context window" (L84). That number is the load-bearing claim of the demo. Read tool results are included in conversation history verbatim (until compaction), so the delta is essentially `file_token_count + small_tool_call_overhead`.

A 3,000-token file gives:
- Tool call request + result envelope: ~50 tokens
- File contents: ~3,000 tokens
- Assistant acknowledgement after the read: ~50-150 tokens

**EXPECTED DELTA from invocation 2: +3,000-3,300 tokens.** [unverified — recommend instructor confirms by checking `wc -w` on `context-window-guide.md` and multiplying by ~1.3 for token count, or running the demo once and recording the actual readout]

Pedagogical hook: "One `Read` just added more tokens than the entire prior conversation."

## Comparison

| Invocation | Trigger | Estimated cumulative tokens | Estimated delta from prior | Confidence |
|---|---|---|---|---|
| 1 | Fresh `claude` launch | ~12-18k | n/a (baseline) | low — depends heavily on Claude Code version |
| 2 | After capital-of-Portugal Q&A | ~12-18k + ~200 | +100-300 | medium — Q&A turn sizes are well-bounded |
| 3 | After Read of context-window-guide.md | ~15-21k + ~3,000 | +3,000-3,300 | high — file size is the dominant term and is fixed |

The instructor only needs *one* number to land per invocation to make the pedagogy work: the **delta**, not the absolute. Deltas are far more stable across Claude Code versions than absolute baselines.

## Decision

**Recommendation: pre-measure during a dry-run, then commit the actual deltas to the guide. Do not ship estimates.**

Rationale:

1. **The pedagogy is the delta, not the absolute number.** "+3,000 tokens from one file read" is the line that lands. If the instructor confidently says "+3,000" and the screen shows "+2,847" or "+3,412", the demo is fine — students see the order of magnitude. If the instructor says "ship the estimate" and the screen shows a wildly different number, credibility erodes mid-demo.

2. **Estimates are fragile across versions.** Anthropic updates the Claude Code system prompt and built-in tool definitions in nearly every release. A guide annotated with `EXPECTED: ~14,000 tokens at baseline` will be wrong within weeks. Deltas (`+~3,000 after the Read`) are far more stable because they're dominated by the file contents, which the instructor controls.

3. **The dry-run is cheap and one-time.** ~10 minutes of the instructor's prep time produces numbers that ship in the guide for the lifetime of this Session 1 lesson.

**Concrete dry-run protocol** (add this as an instructor note in the guide, *not* hard-coded numbers):

```
Before the first time you teach this session:
1. Run Demo 1 end-to-end in a fresh shell.
2. Record the three /context readouts.
3. In this guide, replace each "EXPECTED DELTA" stub with:
   EXPECTED DELTA: ~X tokens added (your dry-run showed Y)
4. Re-run the dry-run any time you upgrade Claude Code (claude --version).
```

This frames the deltas as instructor-calibrated, not authoritative — which is honest and avoids future-Claude or future-Lucas trusting stale numbers.

**Alternative considered and rejected:** "Watch this number drop" framing without specific deltas. Rejected because Demo 1's whole point is that the numbers are *big* and *grow fast*. Vague framing loses the punch of "+3,000 from one file."

## Open questions

- Does the current repo's `CLAUDE.md` cause `claude` to auto-load the agent tool described in it, and does that increase the baseline? Worth checking in the dry-run — if the tool definition (or any MCP servers Lucas has globally configured) adds significant tokens, the baseline shifts.
- Should the guide also annotate Demo 2's `/cost` outputs (the "Attention Is All You Need" PDF read)? The briefing only mentions `/context`, but the same dry-run captures both for free.

## Sources

- [Live demo guide (this repo)](../demos/ctx-engineering-principles-claude-code/live-demo-guide.md) — the file being annotated
- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) — confirms `/context` is a built-in introspection command
- [claude-code-system-prompts (Piebald-AI)](https://github.com/Piebald-AI/claude-code-system-prompts) — third-party reverse-engineering of Claude Code's system prompt size; basis for the ~12-18k baseline estimate
