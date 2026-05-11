# Course Improvement Guide — Context Engineering Hands-On

A structured review of the O'Reilly course **Hands-On Context Engineering** as it currently stands in this repo, with concrete improvements focused on **slide simplification**, **flow**, and **content density**.

The headline finding: the underlying material is strong and well-sourced, but the deck is over-stuffed for a live training. Most fixes are subtraction, not addition.

---

## 1. The Big Picture

| Dimension | Current | Target |
|---|---|---|
| Total slides | **108** (Sessions 1-4 built; S5 unbuilt) | **~70-80** across all 5 sessions |
| Avg. slides per session | ~25-28 (60 min) | ~14-16 (60 min) |
| Avg. time per slide | ~2 min (with demo) → realistically ~1 min on busy slides | ~3-4 min — room to breathe |
| Dominant slide layout | 4-card grid with 2-3 sentences per card | Mix: single-image, single-quote, single-stat, diagram, table |
| Text density per card | High (often a mini paragraph) | One bolded phrase + short caption |

**Why this matters.** O'Reilly live training is a *talk-around-slides* format. When the slide already says it, the instructor either reads aloud (boring) or improvises off-script (slide becomes wallpaper). Sparse slides force the instructor to be the source of meaning — that's where the energy comes from.

---

## 2. Course-Wide Issues (Fix Once, Apply Everywhere)

### 2.1 Redundancy across sessions

The same concepts get re-taught at section starts. Each "Where We Left Off" recap slide repeats material from prior sessions in 4-card form.

| Concept | Where it appears today | Recommended home |
|---|---|---|
| W / S / C / I framework | S1 (slides ~23, 26) → S2 recap → S3 recap → S4 recap | **Introduce in S1; reference by name only afterward** |
| "Bigger windows ≠ better" | S1 ("Bigger Windows ≠ Better") + S3 ("Bigger Windows Don't Solve the Problem") | **One slide, in S3** (where it sets up the failure modes) |
| Context Rot | S1 ("Context Rot") + S4 ("Three Context Problems — Manus") | **Define in S1; cite Manus in S4 as production evidence** |
| 4 Failure Modes | S1 ("Four Context Failure Modes" preview) + S3 (full deep dive) | **Cut from S1 entirely.** Let S3 be the reveal. |
| Static-to-Dynamic Spectrum | S4 ("Spectrum") + S4 ("Spectrum: Full View") | **Merge into one slide** |
| "Three Pillars" (Storage/Management/Usage) | S1 (slide ~17) | **Delete.** It's a parallel taxonomy that competes with W/S/C/I and never gets reused. |

**Estimated savings: 8-12 slides.**

### 2.2 Section-divider slide bloat

Each session has 6-8 numbered "SECTION 0X — Title" dark slides. For 4 sessions that's **~28 divider slides** with no content. They look professional in a PDF, but in a live talk they're transitional whitespace.

**Recommendation:** keep one divider per session (the session-opener title slide). Replace mid-session dividers with **a single line on the next content slide** (e.g., a small "02 / The Agent Loop" eyebrow above the headline). Saves ~20 slides instantly.

### 2.3 The 4-card grid is overused

Nearly every concept slide is a 4-card grid. The pattern becomes monotonous, and each card carries 2-3 sentences which makes the slide read like a paragraph in a 2×2 box.

**Mix in these alternative layouts:**

- **Single-stat hero** — one number (e.g., `46.9%`) filling the slide, one-line caption, source.
- **Single-quote slide** — one Lance Martin / Drew Breunig / Peak Ji pull quote, attribution, and nothing else.
- **Diagram-only** — the diagram *is* the slide; the instructor narrates.
- **Two-column compare** — Before/After, Naive/Engineered, Read/Write tasks. Already used well on the "Read vs Write" slide; do more.
- **Tables** for taxonomies (failure → fix mapping) — already used in Session 4 "Pattern Selection Guide" and works well.

### 2.4 Citation footers

Every content slide has `[1] Source — [2] Source` footers. Useful in the published PDF. **Distracting** during live presentation.

**Recommendation:** strip footers from the live-presentation version of the deck. Keep them in a separate `*-handout.pdf` build. (If the build pipeline is from HTML, gate the footer behind a `?presenter` query param or build flag.)

### 2.5 Density inside cards

Compare the current Session 3 "Failure 01: Context Poisoning" slide:

> "When a hallucination makes it into the context, where it is repeatedly referenced." Errors compound — the agent treats its own prior output as ground truth.
> [Gemini Plays Pokemon — 4 sentences]
> [Why It's Dangerous — 3 sentences]
> [4 symptom callouts]
> [Anthropic quote]
> [2 source footers]

That's ~120 words on one slide. **Target: 25-40 words per slide.** Pull the Gemini Pokemon story into instructor notes; let the slide carry the **name + symptom + quick example anchor** only.

---

## 3. Per-Session Recommendations

### Session 1 — Introduction to Context Engineering (60 min)

**Current:** 33 slides covering attention math, transformer arch, the 3 walls, "what is CE", CE-vs-prompt-eng, evolution, 3-pillars, context window, budget problem, big windows, context rot, 4 failures, 4 operations, write/select/compress/isolate, prioritization, contrarian twist, takeaways, references, transition.

**Issues:**
- **Redundant taxonomies** — "Storage/Management/Usage" pillars vs. "Write/Select/Compress/Isolate" operations vs. "Keep Active/Store Externally/Compress/Reserve" budget. Three overlapping 4-bucket frameworks in one session.
- **Attention math may be too deep for the audience.** Prerequisites only require "basic LLM and AI agent experience." Q·Kᵀ/√dₖ and O(n²·d) complexity will land for some students and lose others. Consider keeping only the **attention-as-relevance-map** intuition and **one** cost claim ("more tokens = more competing relationships").
- **The 4 failure modes preview** anticipates Session 3. Cut it; let Session 3 own the reveal.
- **The "Contrarian Twist — Don't Build Multi-Agents"** slide belongs in Session 2 (where multi-agent patterns are taught), not Session 1.

**Proposed cut list:** Encoder/Decoder reveal duplicate (one slide), Three Pillars, Four Failure Modes preview, Contrarian Twist, one of the two "f(a,b,c…)" recap slides. **Net: -5 to -7 slides.**

**Proposed flow (15-17 slides):**
1. Title
2. Hook: "How do you get good outputs from LLMs?" (the `f(a,b,c…)` framing)
3. One-slide attention intuition (relevance map; skip the math)
4. The wall every developer hits (3-card)
5. What is Context Engineering (definition + entropy quote)
6. Prompt eng vs. context eng (the Anthropic diagram)
7. Section: Context as RAM
8. The context window (CPU/RAM/Disk metaphor)
9. Bigger windows ≠ better (4-symptom card)
10. Context Rot (single slide; the 4 hygiene actions stay)
11. Section: The Four Operations
12. W / S / C / I (4-card — the *one* time this layout is essential)
13. Quick examples slide for each operation (one combined slide, not four)
14. Prioritization rule (Critical/Helpful/Optional)
15. Takeaways (5 → 3)
16. What's next: Session 2

---

### Session 2 — Engineering Context in Agentic Systems (60 min)

**Current:** Built (per memory: 28 slides). Reviewed slides cover "Where We Left Off", chat→agent shift, naive agent problem, agent loop, plus expected sections on Write/Select/Compress/Isolate in agents, multi-agent debate, static context files, takeaways, references, transition.

**Issues:**
- **"Where We Left Off"** repeats S1 content in 4 cards. Replace with a **15-second verbal recap** + one transition slide pointing forward, *not* backward.
- **Static Context Files appears here AND in Session 4.** Decide which session owns it. Recommendation: **own it in Session 4** (where the ETH Zurich study and the static→dynamic spectrum live). Remove from Session 2.
- **Sub-Agents & Sandboxes + Inter-Agent Communication + Multi-Agent Debate** are three slides making overlapping points. Compress to **one slide** ("When sub-agents help, when they hurt") plus the existing Read-vs-Write 2-col slide.
- The "Naive Agent Loop" slide previews failure modes (poisoned history, attention dilution) that belong in Session 3. Just say *"context piles up — we'll dissect why next session"* and move on.

**Estimated savings: -6 to -8 slides → target ~18-20 slides.**

### Session 3 — Diagnosing & Fixing Context Failures (60 min)

**Current:** Built (per memory: 23 slides). 4-failure-mode taxonomy, deep dives, fix mapping, observability, debugging checklist.

**Issues:**
- **Each failure deep-dive slide is the densest in the deck** (~120 words per slide — Poisoning, Distraction, Confusion, Clash). Each currently has: definition + research evidence + mechanism/why-dangerous + 4 symptom callouts + diagnostic + Anthropic quote + 2 source footers.
- **Recommended structure for each failure (2 slides instead of 1 dense slide):**
  - Slide A: **Name + one-sentence definition + one concrete example** (e.g., "Gemini Plays Pokemon: hallucinated game state poisoned future reasoning"). Big visual, sparse text.
  - Slide B: **The fix** — which W/S/C/I lever applies and what it looks like in code. This is what the notebook demonstrates anyway.
- This restructure actually keeps the slide count similar (4×2 = 8 vs. 4×1 = 4) but **doubles the airtime per concept** by splitting density. The hands-on notebook (the actual deliverable) carries the depth.
- **The "Bigger Windows Don't Solve the Problem" slide is a duplicate of Session 1's same point.** Cut it — students saw it 60 minutes ago.

**Estimated changes: net ~0 slides, but much more breathable.**

### Session 4 — Context Engineering Patterns in Modern AI Apps (60 min)

**Current:** Built (per memory: 24 slides). Static-to-dynamic spectrum, ETH study, context priming, Cursor, Agent Skills, Manus harness, tool design, full-spectrum synthesis, pattern selection guide.

**Issues:**
- **Static-to-Dynamic Spectrum appears twice** (intro overview slide + "Full View" synthesis). Merge into one. The synthesis version with the 46.9% / +20% / etc. annotations is the keeper.
- **Manus content is over-weighted.** Currently: "Three Context Problems", "Strategies 1-3", "Strategies 4-5" — three slides on Manus alone. Compress to **one Manus slide** with the 5 strategies as a tight list + one quote, and **one slide** on the three problems mapped explicitly to S3's failure modes ("Rot ≈ Distraction, Pollution ≈ Confusion, Confusion ≈ Clash" — that mapping is the actual insight, lead with it).
- **"Agent Skills: Loadable Knowledge Modules"** slide has a category list (Foundational/Architectural/Operational/Methodology/Cognitive) crammed in alongside three blocks of body text. The Vercel "17 tools → 2 primitives" stat is the gold here — make it a **single-stat slide** and move the category list to the handout.
- **"Tool Design & Token Economics"** is excellent (token-multiplier table is one of the best slides in the deck). Keep as-is.

**Estimated savings: -3 to -5 slides → target ~18-20 slides.**

### Session 5 — Tools and Techniques (45 min)

**Current:** Not built. README says "coming soon"; presentation has the transition slide only.

**Recommendation:**
- Lean **heavily on demo time** — this is a 45-min session, not 60. **8-10 slides max.**
- Structure:
  1. Title + framing ("everything you've learned, applied with your day-to-day tools")
  2. The Claude Code primitives map (CLAUDE.md, slash commands, hooks, sub-agents, MCP) — one slide, one diagram
  3. Live demo (~20 min) — extend the existing `live-sesh-agent-claude-code` agent or build a new one that shows hooks + sub-agents + MCP together
  4. One slide each for: hooks pattern, custom slash commands, MCP integration
  5. The cheatsheet (existing PDF) — show it on screen; tell students it's in the repo
  6. Putting it all together: a "build your own playbook" closing slide
  7. Course wrap + Q&A pointer

**The cheatsheet PDF (`assets/context-engineering-tools-cheatsheet.pdf`) IS the deliverable for Session 5.** Slides should support it, not duplicate it.

---

## 4. Demo & Repo Improvements

### 4.1 Session 1 live demo

`demos/ctx-engineering-principles-claude-code/live-demo-guide.md` is solid (~30 min, 5 demos). One issue: it uses `~3,000 tokens` worth of file reads to demonstrate context growth. **Add `/context` token deltas as expected output in the guide** so the instructor isn't squinting at the screen during the demo.

### 4.2 `chat-with-artifacts`

Has a stray `structured_outputs_demo.py` not mentioned in the README. Either:
- Reference it in the README as a Session 4 standalone teaching aid, or
- Delete it if it's superseded by `app.py`.

### 4.3 Session 5 demo placeholder

`demos/ctx-engineering-tools-claude-code/` is empty. Concrete suggestion: a **single Claude Code project** that demonstrates:
- A minimal `CLAUDE.md` (the ETH Zurich-validated "10-20 lines" version)
- One custom slash command (`/audit-context`) that runs the `agent_tool_for_claude_code.py` agent
- One hook (post-tool-use) that writes tool outputs to a sidecar file (the Cursor "tool response files" pattern)
- One MCP server hookup (use one of the user's existing MCP configs)

This becomes the live-codable artifact students leave with.

### 4.4 README

The README is thorough but **300+ lines and front-loads troubleshooting**. Move troubleshooting to the bottom (already done — good). Consider adding a **2-line TL;DR at the top**: "5 sessions, 4 runnable demos, 1 notebook. `export ANTHROPIC_API_KEY=… && cd demos/<name> && uv run app.py`."

### 4.5 Stale memory in `MEMORY.md`

`MEMORY.md` claims `presentation/01-…pptx` through `presentation/04-…pptx` exist, built via `workspace-s2/` etc. **Neither the .pptx files nor the workspace dirs exist on disk.** Either:
- Restore them (if they were accidentally `.gitignore`d or moved), or
- Update `MEMORY.md` to reflect that the live deck is a single `.key`/`.pdf`.

This will cause confusion in future Claude Code sessions if not reconciled.

---

## 5. The "Less Text, More Organic" Principles (For Slide Rewrites)

When rewriting individual slides, apply these rules:

1. **One idea per slide.** If a slide has two equally-weighted ideas, it's two slides.
2. **The headline is the takeaway.** "Context Rot" is a topic. "Information goes stale — and the agent can't tell" is a takeaway. Use the takeaway form.
3. **Show the evidence, not the explanation.** A stat (`-3%`, `+20%`, `46.9%`, `83.9%`) plus a one-line caption beats a paragraph.
4. **Quotes go alone.** A Lance Martin or Drew Breunig pull quote on its own slide is more memorable than the same quote stuffed in a callout box under three other things.
5. **Diagrams replace lists.** The "Anthropic prompt-vs-context-eng" diagram (slide ~14) does in one image what a 4-card grid would take 80 words to say. Build more of these.
6. **Cut citations from the live deck.** Move them to a published handout PDF. The instructor can mention sources verbally.
7. **If you can't read it from the back of the room, it's too small.** Anything under ~24pt body text is for the handout, not the slide.

---

## 6. Suggested Build Order

If you can only do some of this, do it in this order:

1. **Fix the duplications** (§2.1) — biggest content-quality win, removes student confusion
2. **Cut section-divider slides** (§2.2) — fastest visual improvement, ~20 slides gone
3. **Split Session 3 failure-mode slides** (§3, S3) — most-impactful pedagogy improvement
4. **Build Session 5** (§3, S5) — currently a gap in the deliverables
5. **Reconcile `MEMORY.md`** (§4.5) — prevents future-Claude from making bad assumptions
6. **Strip citation footers from live deck** (§2.4) — easy polish
7. **Rewrite remaining dense slides** (§2.5, §5 principles) — incremental, can be done over multiple passes

---

## 7. What's Already Working (Keep)

To avoid the impression that everything needs changing — these are the strongest parts of the current deck and should be preserved or replicated:

- **The CPU / RAM / Disk metaphor** for the context window (S1) — concrete, memorable, accurate.
- **The "Read vs Write Tasks" 2-column slide** (S2) — the right level of compression.
- **The Pattern Selection Guide table** (S4) — actionable; students will photograph this slide.
- **The token-multiplier table** (S4 "Tool Design & Token Economics") — single best stat in the deck.
- **The hand-drawn `f(a,b,c…)` recap slide** in S1 — visual variety; do more like this.
- **The `live-demo-guide.md` script structure** — instructor-note callouts are well-placed.
- **The hand-rolled agent loop** in `demos/agentic-retrieval/` — this is the right level of abstraction for teaching, no framework magic.

---

*Generated 2026-05-09. References to slide numbers refer to the current `presentation/context-engineering-hands-on.pdf` (108 pages).*
