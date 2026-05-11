# ETH Zurich CLAUDE.md Length Pattern — Verification

## Context

The briefing (`IMPROVEMENTS.md` §4.3) proposes that the Session 5 demo project ship with "a minimal `CLAUDE.md` (the **ETH Zurich-validated** '10-20 lines' version)." Two claims to verify:

1. Is there an ETH Zurich study that evaluates CLAUDE.md / AGENTS.md effectiveness?
2. Does that study (or any other primary source) recommend specifically 10-20 lines as the optimal length?

## Findings

### The ETH Zurich study exists — confirmed

**Paper:** "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"
**Authors:** Thibaud Gloaguen, Niels Mündler, Mark Müller, Veselin Raychev, Martin Vechev (ETH Zurich + LogicStar.ai)
**Published:** February 12-13, 2026
**ArXiv:** 2602.11988

[source: https://arxiv.org/abs/2602.11988]

The study evaluates four coding agents (including Claude Code) across 300 SWE-bench Lite tasks plus a new 138-task benchmark called **AGENTbench**. [source: https://arxiv.org/abs/2602.11988, https://medium.com/@reliabledataengineering/claude-md-dont-work-eth-zurich-study-shows-context-files-reduce-success-rates-by-3-1518cac80929]

### Key empirical findings (and they're not flattering for CLAUDE.md)

- **LLM-generated context files (the kind `/init` produces) make things *worse***: ~3% drop in task success rate, ~20% increase in inference cost. [source: https://arxiv.org/abs/2602.11988]
- **Human-written context files give marginal gains**: ~4% improvement on AGENTbench, but with ~19% cost increase from extra exploration steps. [source: https://medium.com/@reliabledataengineering/claude-md-dont-work-eth-zurich-study-shows-context-files-reduce-success-rates-by-3-1518cac80929]
- **Agents do *more* (27% more testing, more grep, more file reads) but don't actually solve more tasks** when given context files. [source: https://medium.com/@reliabledataengineering/claude-md-dont-work-eth-zurich-study-shows-context-files-reduce-success-rates-by-3-1518cac80929]

### The "10-20 lines" claim — NOT in the ETH Zurich paper

Direct WebFetch of the arXiv abstract confirms: **the paper does not recommend "10-20 lines"** as a specific length. Its guidance on length is qualitative:

- "human-written context files should describe only minimal requirements" [source: https://arxiv.org/abs/2602.11988]
- Third-party summary: "Aim for <200 words. Focus on things agents can't discover." [source: https://medium.com/@reliabledataengineering/claude-md-dont-work-eth-zurich-study-shows-context-files-reduce-success-rates-by-3-1518cac80929]

A separate summary cites "<80 lines" as a community/research convergence point, but attributes that to "the sweet spot from community benchmarks, the research, and Anthropic's own internal usage" — i.e. a synthesized recommendation, not a single ETH Zurich claim. [source: https://medium.com/@reliabledataengineering/claude-md-dont-work-eth-zurich-study-shows-context-files-reduce-success-rates-by-3-1518cac80929]

**Bottom line: the phrase "ETH Zurich-validated 10-20 lines pattern" is not supported by the cited primary source.** The paper supports "minimal," "<200 words," and "human-written," not the specific 10-20 line number.

### Where does "10-20 lines" actually come from?

Best guesses (none load-bearing — the briefing author would know):

- A reasonable extrapolation: "<200 words" at typical Markdown line widths (~10-15 words/line) is ~14-20 lines. So 10-20 lines is consistent with the paper's quantitative bound, just not a number the paper uses. [unverified]
- Community lore on Hacker News / Twitter about minimal CLAUDE.md files [unverified]
- Pre-existing Lucas convention in this repo — the current `CLAUDE.md` in this very repo is 14 lines, which fits 10-20 [verified via direct read of repo CLAUDE.md]

### Anthropic's own guidance

Anthropic's Claude Code docs and prompt-engineering best practices recommend concise, specific system instructions but do not publish a specific line-count target for CLAUDE.md. [source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices, https://code.claude.com/docs/en/how-claude-code-works]

## Comparison

| Claim about CLAUDE.md length | Source | Verified? |
|---|---|---|
| "10-20 lines" — specific number | Briefing only | Not in any primary source |
| "<200 words" — qualitative | ETH Zurich paper (per third-party summary) | Verified [source: Medium summary of arXiv 2602.11988] |
| "Minimal, only non-inferable details" | ETH Zurich paper (direct WebFetch of abstract) | Verified |
| "<80 lines" — convergence point | Community synthesis (Medium summary) | Verified as third-party claim, not as ETH Zurich's claim |
| "Human-written outperforms LLM-generated" | ETH Zurich paper | Verified |

## Decision

**Recommendation: option (b) reframe with what the source actually says.** Drop the literal phrase "ETH Zurich-validated 10-20 lines pattern" from the briefing / Session 5 materials. Keep the *minimal CLAUDE.md* idea — it's good — but cite it accurately.

**Proposed replacement language for the Session 5 demo and any slide referencing this:**

> "A minimal, human-written CLAUDE.md (~15 lines / <200 words). ETH Zurich's AGENTS.md study (Feb 2026) found that **shorter, human-written context files outperform LLM-generated ones**, and that the most successful files contain only information agents can't discover on their own."

This is accurate, attributable, and pedagogically stronger than "ETH Zurich-validated 10-20 lines" because it tells students *why* short is better, not just *that* short is better.

**For the actual demo `CLAUDE.md` file in `demos/ctx-engineering-tools-claude-code/`:**

- Target ~10-20 lines (matches what the briefing wants, matches existing repo convention, and falls inside the paper's <200-word qualitative bound).
- Content should be **only what the agent can't infer from the repo itself**: the project's purpose, the one-line description of how to run things, any non-obvious conventions. Avoid restating the directory structure (the agent can `ls`).
- Use the existing repo's `CLAUDE.md` (14 lines, mostly project purpose + one custom instruction about the agent tool) as a template — it already fits the ETH Zurich recommendation.

**Bonus pedagogical move:** the Session 5 slide on CLAUDE.md could *lead with the counter-intuitive ETH Zurich finding* — "Most CLAUDE.md files make agents worse" — and then resolve with "Here's the pattern that actually helps." That tension is more memorable than a length rule. The briefing's own §5.2 principle ("the headline is the takeaway") supports this framing.

**Why not option (a) — drop the framing entirely?** The ETH Zurich result is genuinely useful evidence for the Session 5 lesson. Dropping it would lose a strong external citation. The fix is to attribute correctly, not to remove.

**Why not option (c) — flag the briefing claim for removal without replacement?** Same reason — there's a real, citable, recent study (Feb 2026) that supports the pedagogy. Just not with the specific words the briefing uses.

## Open questions

- Was the briefing author thinking of a different source for "10-20 lines"? Worth a quick check before Session 5 ships. If they have a source we missed, fold it in; if not, the reframe above stands.
- Should Session 5 reference the ETH Zurich paper directly (arXiv link) or via a more accessible secondary summary? Recommend the arXiv link in the handout, a verbal "ETH Zurich, Feb 2026" mention in the live talk.
- Does the AGENTbench dataset cover Python repos similar enough to this course's demos to use it as a benchmark for the Session 5 demo's own CLAUDE.md? Probably not worth the rabbit hole, but flagging.

## Sources

- [Evaluating AGENTS.md (arXiv 2602.11988)](https://arxiv.org/abs/2602.11988) — primary source, ETH Zurich Feb 2026
- [arXiv HTML version](https://arxiv.org/html/2602.11988v1) — same paper
- [InfoQ — coverage of the AGENTS.md study](https://www.infoq.com/news/2026/03/agents-context-file-value-review/)
- [Medium — Claude.md Don't Work (Reliable Data Engineering)](https://medium.com/@reliabledataengineering/claude-md-dont-work-eth-zurich-study-shows-context-files-reduce-success-rates-by-3-1518cac80929) — third-party summary with the "<200 words" / "<80 lines" framings
- [Straion — Your AGENTS.md is costing more than you think](https://straion.com/blog/delete-your-claude-md-science-says-so/)
- [Anthropic Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
- This repo's existing `CLAUDE.md` (14 lines) — already conforms to the recommended pattern
