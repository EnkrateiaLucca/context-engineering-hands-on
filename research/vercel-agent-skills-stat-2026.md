# Vercel "Removed 80% of Our Agent's Tools" — Source & Phrasing

## Context

The briefing (`IMPROVEMENTS.md` §3 / Session 4) wants to use a Vercel-published stat — informally summarized as "17 tools → 2 primitives = 80% → 100%" — as a **single-stat hero slide** for the Agent Skills section. The brief asks: confirm exact phrasing, methodology, model, date, and whether "Agent Skills" is the right framing or a different framing should be used.

## Findings

### Source — confirmed primary

The stat comes from Vercel's engineering blog post **"We removed 80% of our agent's tools"** by the Vercel team, published **December 22, 2025**. [source: https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools]

Cross-verified by Vercel's own X/Twitter announcement: "We improved our text-to-SQL agent by removing 80% of its tools and adding a sandbox. 40% fewer tokens, 40% fewer steps, 3.5x faster." [source: https://x.com/vercel/status/2003218088435851441]

### Exact stats (per the Vercel post, verified via WebFetch)

The system in question is **d0**, Vercel's internal text-to-SQL agent.

- **Tools removed**: from 15 specialized tools down to a single bash command execution tool (per the Vercel post text). [source: https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools]
- **Success rate**: 80% → 100% (4-of-5 → 5-of-5 on a 5-query benchmark)
- **Execution time**: 274.8s → 77.4s (3.5× faster)
- **Tokens**: ~102,000 → ~61,000 (~37% reduction; Vercel rounds to "40% fewer" in marketing)
- **Steps**: ~12 → ~7 (42% fewer)
- **Model used**: Claude Opus 4.5 [source: https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools]
- **Eval methodology**: "5 representative queries" [source: https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools, https://www.zenml.io/llmops-database/simplifying-text-to-sql-agents-by-removing-80-of-tools]

### A note on the "17 tools" / "2 primitives" framing in the briefing

The briefing's "17 → 2" version is **slightly off from the primary source**, where multiple numbers float around because the eval evolved across iterations:

- Vercel's own post headlines **15 specialized tools → 1 bash tool** ("removed 80%"). [source: https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools]
- Secondary summaries (Pulumi, ZenML, the Vercel-D0 architecture descriptions) cite **17 tools → 2 primitives (ExecuteCommand + ExecuteSQL)**, treating the SQL execution as a separate primitive. [source: https://www.pulumi.com/blog/self-verifying-ai-agents-vercels-agent-browser-in-the-ralph-wiggum-loop/, https://www.zenml.io/llmops-database/simplifying-text-to-sql-agents-by-removing-80-of-tools]
- One ZenML summary says **18 tools → 2 tools**. [source: https://www.zenml.io/llmops-database/simplifying-text-to-sql-agents-by-removing-80-of-tools]

The 80% → 100% success-rate delta is consistent across all summaries. The "X → Y" count varies because different sources count "and a SQL execution wrapper" as either a separate tool or as part of the bash primitive. The Vercel post itself is the most conservative: "15 → 1, 80% removal."

### Is "Agent Skills" the right framing for this slide?

**No.** "Agent Skills" is **Vercel's other terminology** — used in a different Vercel blog post ("AGENTS.md outperforms skills in our agent evals", January 27, 2026) [source: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals] and in the `vercel-labs/agent-skills` repo [source: https://github.com/vercel-labs/agent-skills]. That work is about packageable AGENTS.md / skill bundles — a separate concept from the d0 tool-consolidation story.

Calling this stat an "Agent Skills" stat conflates two different Vercel publications. The right framing is **tool consolidation** or **fewer-tools-more-success** — which is what the briefing actually wants pedagogically. The slide title should reflect that.

## Comparison — how different sources report the same eval

| Source | Tool count claim | Success rate | Model | Confidence |
|---|---|---|---|---|
| Vercel blog (primary) | 15 → 1 | 80% → 100% | Claude Opus 4.5 | High |
| Pulumi summary | 17 → 2 (ExecuteCommand + ExecuteSQL) | 80% → 100% | Not stated | Medium |
| ZenML summary | 18 → 2 | 80% → 100% | Not stated | Medium |
| Vercel tweet | "removed 80% of tools" | not numerical | Not stated | High |

**Single source of truth for the slide: the Vercel blog post (Dec 22, 2025).** Anything else is a re-summary.

## Decision

**The stat is strong enough to anchor a single-stat slide, but use Vercel's own framing — not the briefing's "17 → 2" version — and add one caveat.**

**Recommended slide content** (one screen):

> # 80% → 100%
>
> Vercel removed 80% of their text-to-SQL agent's tools.
> Success rate went up. Tokens, steps, and latency went down.
>
> *Vercel Engineering, Dec 2025 · 5-query benchmark · Claude Opus 4.5*

**Why this works:**

1. The headline number is the success-rate jump, which is unambiguous and consistent across every source.
2. "80% → 100%" is more visually punchy than "15 → 1" or "17 → 2" — exactly what a single-stat hero slide needs.
3. The footer caveat (`5-query benchmark · Claude Opus 4.5`) is honest about scale and lets students who care look it up. The briefing's §2.4 says citation footers should be in the handout — but a single short attribution line for a hero-stat slide is appropriate even on the live deck, because it inoculates against "where did that number come from?" pushback.

**The one caveat:** 5 queries is a tiny eval. The instructor should be ready for this if a student asks. Suggested verbal answer: *"Yes, it's a small benchmark. The point isn't that 100% is the new reality — it's that going from many specialized tools to a few flexible ones consistently improves agent performance, which Anthropic's own tool-design guidance also recommends. Vercel's stat is a vivid example of a pattern, not a definitive measurement."*

**Section context:** This slide does NOT belong in an "Agent Skills" section. It belongs in a **tool design / token economics** section (which the briefing notes is "one of the best slides in the deck" — Session 4's existing token-multiplier table). The two slides reinforce each other: the table shows *why* fewer/smarter tools help, the Vercel stat shows *that* it works in production.

If the Session 4 deck still needs an Agent Skills slide, use a different anchor stat from `vercel-labs/agent-skills` or the AGENTS.md eval (53% → 100% with AGENTS.md docs index, from the Jan 2026 Vercel post) [source: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals].

## Open questions

- Should the Session 4 slide title be "Fewer tools, better agents" (pattern framing) or "80% → 100%" (stat-first framing)? The briefing's §5.3 principle ("show the evidence, not the explanation") favors stat-first.
- The briefing's reference to "17 tools → 2 primitives" likely came from one of the secondary summaries (Pulumi/ZenML). The instructor should be aware of this when fielding student questions — if a student looks up the Vercel post directly, they'll see "15 → 1." Recommend the slide use Vercel's own numbers to avoid the discrepancy.

## Sources

- [Vercel — We removed 80% of our agent's tools (Dec 22, 2025)](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools) — primary source
- [Vercel on X — announcement tweet](https://x.com/vercel/status/2003218088435851441)
- [Pulumi blog — Self-Verifying AI Agents](https://www.pulumi.com/blog/self-verifying-ai-agents-vercels-agent-browser-in-the-ralph-wiggum-loop/) — secondary summary using "17 → 2" framing
- [ZenML LLMOps Database — Simplifying Text-to-SQL Agents](https://www.zenml.io/llmops-database/simplifying-text-to-sql-agents-by-removing-80-of-tools) — secondary summary using "18 → 2" framing
- [Vercel — AGENTS.md outperforms skills in our agent evals (Jan 27, 2026)](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals) — separate Vercel publication; this is what "Agent Skills" actually refers to
- [vercel-labs/agent-skills (GitHub)](https://github.com/vercel-labs/agent-skills) — Vercel's Agent Skills repo (different concept from the d0 stat)
