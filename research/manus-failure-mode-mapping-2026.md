# Manus Failure-Mode Mapping vs. Breunig's Four Failures

## Context

The Session 4 consolidation rewrite (briefing `IMPROVEMENTS.md` §3 / Session 4) wants to compress the three Manus slides into one, with the **headline insight**:

> "Rot ≈ Distraction, Pollution ≈ Confusion, Confusion ≈ Clash"

— mapping Manus's three context problems onto Drew Breunig's four failure modes (the Session 3 taxonomy). The question is whether this mapping is defensible against the actual published Manus / Peak Ji writing, or whether it's the briefing author's synthesis that needs to be attributed accordingly.

## Findings

### Breunig's four failure modes — confirmed verbatim

Drew Breunig, "How Long Contexts Fail" (2025-06-22):

- **Context Poisoning**: "When a hallucination or other error makes it into the context, where it is repeatedly referenced." [source: https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html]
- **Context Distraction**: "When a context grows so long that the model over-focuses on the context, neglecting what it learned during training." [source: https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html]
- **Context Confusion**: "When superfluous content in the context is used by the model to generate a low-quality response." [source: https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html]
- **Context Clash**: "When you accrue new information and tools in your context that conflicts with other information in the context." [source: https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html]

The Session 3 deck already uses these four terms with this attribution. No issue there.

### Peak Ji / Manus's actual language — does NOT match the "rot/pollution/confusion" triad

The canonical Manus blog post, "Context Engineering for AI Agents: Lessons from Building Manus" by Yichao "Peak" Ji (manus.im/blog), **does not use the terms "context rot," "context pollution," or "context confusion" to label its failure modes.** Direct review of the post confirms these specific three terms do not appear as a named triad. [source: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus]

What the Manus post actually discusses:
- KV-cache hit rate as the primary production constraint
- "Mask, don't remove" tools (action-space stability across iterations)
- File system as ultimate context
- Recitation (re-stating goals to combat lost-in-the-middle)
- Keeping wrong turns in context (so the model learns from its own errors)
- The Bitter-Lesson critique of over-engineering the harness

[source: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus]

### Where "context rot" actually comes from in the Manus ecosystem

Lance Martin's write-up of Peak Ji's follow-up talk ("Context Engineering in Manus", 2025-10-15) attributes "context rot" to **Chroma's research**, not to Manus itself: "Chroma has a great study on context rot" and Manus uses context engineering to address it. The three things Manus's post-original-blog-post talk actually frames as their playbook are **strategies, not failures**: Reduce, Offload, Isolate. [source: https://rlancemartin.github.io/2025/10/15/manus/]

### Where the "rot / pollution / confusion" triad actually comes from

The triad does appear in third-party summaries of Manus content — e.g. one DEV.to summary attributes "Context Pollution" and "Context Confusion" as patterns the Manus post warns about [source: https://dev.to/contextspace_/context-engineering-for-ai-agents-key-lessons-from-manus-3f83]. But these are the summarizer's labels imposed on Peak Ji's content, not Peak Ji's own terminology. The original Manus post does not name a "three problems" framework with these names. [unverified — the briefing's exact triad as a unit may originate with the briefing author or with a third-party summarizer; not traced to Peak Ji directly]

### The mapping itself — is it defensible?

Putting aside provenance, do the conceptual mappings hold?

| Briefing claim | Plausibility | Assessment |
|---|---|---|
| Rot ≈ Distraction | Strong | Both describe quality degrading as the window fills with semantically-similar-but-irrelevant content. Chroma's rot study + Breunig's distraction definition (over-focusing on long context, neglecting training) are nearly the same phenomenon from different angles. |
| Pollution ≈ Confusion | Medium | "Pollution" in informal usage means noise in the window dragging quality down — close to Breunig's Confusion ("superfluous content used to generate low-quality response"). Defensible. |
| Confusion ≈ Clash | Weak | This one breaks. If "Confusion" in the Manus framing means *the agent gets confused by too many overlapping tool definitions* (consistent with the "Hierarchical Action Space" Lance summarizes), that's closer to Breunig's Confusion or even Poisoning, not Clash (which is specifically about conflicting information/tools). The mapping forces a 3→4 reduction that doesn't sit cleanly. |

## Decision

**Recommendation: (b) instructor-proposed synthesis, with both sources cited. Reframe the slide accordingly — and consider dropping the third mapping pair.**

Specifically:

1. **Do not present this as "Peak Ji's mapping."** It isn't. Peak Ji's post does not name a rot/pollution/confusion triad. Attributing the mapping to him is a verifiable misattribution that could be caught by any student who reads the source.

2. **Do present it as instructor synthesis** — the headline could be something like *"Manus's production problems map onto Breunig's failure modes"* (instructor framing), with two clean attributions on the slide: one to Breunig (the four failures), one to Peak Ji / Manus (the production lessons). The mapping arrows are the instructor's editorial bridge.

3. **Drop "Confusion ≈ Clash" from the slide.** It's the weakest of the three pairings and the one most likely to invite "wait, what?" from an attentive student. Keep:
   - Rot → Distraction (the strongest pair, well-supported by Chroma research)
   - Pollution → Confusion (defensible)
   - Replace the third arrow with a note: "Manus's other lessons (action-space hierarchy, KV-cache, recitation) cut across multiple failure modes — see the next slide for the full 5-strategy list."

4. **Slide caption / source line:** `Failure modes: Breunig (2025). Production lessons: Ji / Manus (2025). Mapping: instructor synthesis.` This is honest and a single line of small footer text.

This recommendation aligns with the briefing's own §2.4 guidance ("strip footers from the live deck") — the attribution line stays in the handout, not on the projected slide. The on-slide framing is just the mapping diagram + instructor narrative.

## Open questions

- Is there a *more recent* Manus post (after the October 2025 follow-up) that names a "three problems" triad explicitly? Not found in this round; worth one more pass before Session 4 ships if the instructor wants to keep the triad framing. [unverified]
- Does the briefing author have a different source in mind for the triad attribution? If so, that source should be added to the slide footer.

## Sources

- [Drew Breunig — How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html) — canonical source for the four failure modes
- [Yichao "Peak" Ji — Context Engineering for AI Agents: Lessons from Building Manus (manus.im)](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) — original Manus blog; verified does NOT use the rot/pollution/confusion triad
- [Lance Martin — Context Engineering in Manus (2025-10-15)](https://rlancemartin.github.io/2025/10/15/manus/) — write-up of Peak Ji's follow-up talk; uses "Reduce / Offload / Isolate" framing
- [Peak Ji — Medium version of the Manus post](https://medium.com/@peakji/context-engineering-for-ai-agents-lessons-from-building-manus-71883f0a67f2) — same content as manus.im version
- [DEV.to summary using pollution/confusion framing](https://dev.to/contextspace_/context-engineering-for-ai-agents-key-lessons-from-manus-3f83) — example of a third-party summarizer imposing the triad
