# Live Demo Guide — Context Engineering Principles with Claude Code

### Session 1: Introduction to Context Engineering | O'Reilly Live Training

**Total demo time:** ~30 minutes across 5 demos
**Dual purpose:** Instructor live-demo script + student post-session cheatsheet

*This guide turns the research from the [Context Window Field Guide](context-window-guide.md) into live, reproducible demonstrations using Claude Code. Each demo maps to specific Playbook rules from §6 of the Field Guide.*

---

## Pre-Demo Setup Checklist

Complete these steps **before** the session starts:

- Claude Code installed and working (`claude --version`)
- API key configured (`ANTHROPIC_API_KEY` set)
- This repository cloned and available locally
- Terminal font size set to **18pt+** (audience readability)
- Dark terminal theme (reduces eye strain on projector)
- Supporting files verified:
  - `demos/ctx-engineering-principles-claude-code/long-doc-middle.txt`
  - `demos/ctx-engineering-principles-claude-code/long-doc-top.txt`
  - `assets/attention-paper.pdf`
- Quick verification — run this and confirm a response:

```bash
claude -p "hello"
```

> **INSTRUCTOR NOTE:** If using a shared API key for the session, set it in your shell profile before launching. Students do NOT need API keys — they watch the demos live and follow along with this guide afterward.

---

## Demo 1: Context Is Everything (~5 min)

**Playbook rules demonstrated:** Rule 1 (Lean Context)
**Concept:** Make the invisible visible — students see what's *actually* in the context window before they've even typed anything.

### Steps

**1. Launch a fresh Claude Code session:**

```bash
claude
```

**2. Immediately run `/context`:**

```
/context
```

**WHAT TO EXPECT:** Claude Code displays a structured breakdown of everything currently loaded in the context window — the system prompt, CLAUDE.md instructions (if present), tool definitions, and any conversation history. Students see that the window is *already populated* before they typed a single real question.

> **INSTRUCTOR NOTE:** Pause here. Point at the screen: "You haven't asked anything yet. But look at how much is already loaded — system prompt, tool definitions, CLAUDE.md. This is the invisible cost of context. Every session starts with thousands of tokens already spoken for."

**3. Now do something simple — ask a quick question:**

```
What is the capital of Portugal?
```

**4. Run `/context` again:**

```
/context
```

**WHAT TO EXPECT:** The context has grown — it now includes the question, Claude's response, and any internal reasoning. Even a trivial one-line exchange adds tokens.

**5. Read a file to show a bigger jump:**

```
Read demos/ctx-engineering-principles-claude-code/context-window-guide.md
```

**6. Run `/context` one more time:**

```
/context
```

**WHAT TO EXPECT:** Dramatic jump. The entire file (~3,000 tokens) is now sitting in the context window alongside everything else.

> **INSTRUCTOR NOTE:** Call out the progression: "One question added a little. One file read added *a lot*. Now multiply that by a real working session where you read 10–20 files, run tools, and have a long conversation. Context fills up fast — and everything in it competes for the model's attention."

**KEY TAKEAWAY:** The context window is not just "your messages." It's the system prompt + CLAUDE.md + tool definitions + conversation history + every file read + every tool result. `/context` makes this visible. Understanding what's in the window — and how fast it grows — is the foundation of context engineering.

---

## Demo 2: Context Rot in Action (~7 min)

**Playbook rules demonstrated:** Rule 1 (Lean Context), Rule 3 (New Chat for New Task)
**Concept:** Prove that accumulated irrelevant context degrades output quality — using a realistic scenario, not contrived examples.

### Steps

**1. Start a clean session and establish a baseline — one explanation, one code task:**

```
/clear
```

```
Explain what positional encoding is and why it matters in transformer models. Keep it to 3–4 sentences.
```

> **INSTRUCTOR NOTE:** Note the quality: concise, clear, well-structured explanation. This is the baseline from a clean context. Save or screenshot the output.

```
Write a Python function called cosine_similarity that takes two lists of floats and returns their cosine similarity. Include type hints and a docstring.
```

> **INSTRUCTOR NOTE:** Again, note the quality: clean function, proper type hints, good docstring. Screenshot this too — you'll compare it in a moment.

**2. Check the current cost — this is the "clean" baseline:**

```
/cost
```

**3. Now simulate what actually happens in a real working session — read a large, unrelated document:**

```
Read assets/attention-paper.pdf
```

> **INSTRUCTOR NOTE:** This is the realistic scenario: you were researching one thing, read a paper, and now you want to switch tasks but forget to `/clear`. This happens constantly in real workflows.

**4. Check the cost again — watch the jump:**

```
/cost
```

**WHAT TO EXPECT:** Token count spikes dramatically. The 15-page "Attention Is All You Need" paper just dumped ~15,000+ tokens into the context window. Point at the delta.

> **INSTRUCTOR NOTE:** "That single `Read` command just added more tokens than our entire conversation so far. The paper is about transformers — it's *related* to ML, which makes it worse. Semantically similar but irrelevant content is the most dangerous kind of noise, because the model can't easily ignore it."

**5. Now repeat the same explanation task — same prompt, polluted context:**

```
Explain what positional encoding is and why it matters in transformer models. Keep it to 3–4 sentences.
```

**WHAT TO EXPECT:** The model now has the full Attention paper in context. Its explanation may become more verbose, overly technical, or drift toward the specific sinusoidal encoding from the paper rather than giving a clean general explanation. It may cite implementation details that weren't in the original response.

**6. Repeat the same code task:**

```
Write a Python function called cosine_similarity that takes two lists of floats and returns their cosine similarity. Include type hints and a docstring.
```

**WHAT TO EXPECT:** Compare against the baseline. Look for: different import choices, changed docstring style, added complexity, or subtle quality shifts. The model is now processing 15K+ tokens of paper content alongside your simple function request.

> **INSTRUCTOR NOTE:** Compare both pairs side by side. The key insight: "The same prompts, the same session, but the outputs shifted — because 15,000 tokens of a research paper are now sitting between your question and the model's attention. That's context rot. It's not a dramatic failure; it's a subtle, creeping degradation."

**7. Clear and retry — quality restored:**

```
/clear
```

```
Explain what positional encoding is and why it matters in transformer models. Keep it to 3–4 sentences.
```

```
Write a Python function called cosine_similarity that takes two lists of floats and returns their cosine similarity. Include type hints and a docstring.
```

**WHAT TO EXPECT:** Both outputs return to the quality and style of the originals. Clean context, clean output.

**KEY TAKEAWAY:** Context rot happens in realistic workflows — you read a file for one task, pivot to another, and forget to reset. The Attention paper is *topically related* to the questions, which makes the interference worse (this is the "distractor interference" effect from the Field Guide, §2). `/clear` is your reset button. This is why Rule 3 says: *start a new chat for a new task.*

---

## Demo 3: Lost in the Middle (~5 min)

**Playbook rules demonstrated:** Rule 2 (Front-Load What Matters)
**Concept:** Information position in the context window affects whether the model finds it.

### Steps

**1. Start clean:**

```
/clear
```

**2. Read the document with the fact buried in the middle:**

```
Read demos/ctx-engineering-principles-claude-code/long-doc-middle.txt
```

**3. Ask for the specific fact:**

```
According to this policy document, who is the approved vendor for cloud infrastructure and what is their contract number?
```

**WHAT TO EXPECT:** Claude may find it, but might take longer, hedge, or miss details. The key fact is buried at section 30 of 50 in a ~9,000-word document — deep in the "lost in the middle" zone, surrounded by semantically similar content about vendors, contracts, and procurement.

> **INSTRUCTOR NOTE:** Even if Claude finds it, note any hedging language, delay, or incomplete details. The document is deliberately long (~12,000 tokens) and all the content is about procurement and vendors — making the target fact hard to distinguish from surrounding noise. This is distractor interference compounded by position bias.

**4. Clear and try with the front-loaded version:**

```
/clear
```

```
Read demos/ctx-engineering-principles-claude-code/long-doc-top.txt
```

```
According to this policy document, who is the approved vendor for cloud infrastructure and what is their contract number?
```

**WHAT TO EXPECT:** Claude finds the answer immediately and confidently — "Meridian Corp, Contract #MC-2847." The fact is at paragraph 2, right in the high-attention zone.

**5. Reveal the trick:**

> **INSTRUCTOR NOTE:** Tell the students: "These are the *exact same document* — same 50 sections, same 9,000 words. The only difference is where the key fact appears. In the first version, it's buried at section 30 of 50 — the dead center. In the second, it's at section 2. Same question, same content, different result — because *position matters.* And this document is deliberately all about vendors and contracts, so every section looks semantically similar to the target fact. That's the worst case for retrieval."

**KEY TAKEAWAY:** Front-load what matters. This is the "Lost in the Middle" effect from the Liu et al. research (§3 of the Field Guide) — models attend most strongly to content at the beginning and end, and poorly to content in the middle. The effect is amplified when surrounding content is semantically similar (distractor interference). When you control the input, put the important information first.

---

## Demo 4: Grounding vs Memory (~5 min)

**Playbook rules demonstrated:** Rule 4 (Ground in Source Material), Rule 7 (Push Back on Confidence)
**Concept:** Models are more accurate extracting from documents than recalling from training data — and grounded models resist pushback better.

### Steps

**1. Start clean:**

```
/clear
```

**2. Ask a specific factual question from memory:**

```
What was the BLEU score achieved by the Transformer base model on the WMT 2014 English-to-German translation task, as reported in the "Attention Is All You Need" paper?
```

**WHAT TO EXPECT:** Claude will answer confidently — likely citing a specific number. It may or may not be correct. The key observation: the model *sounds certain* regardless.

> **INSTRUCTOR NOTE:** Note the confidence level. Whether the number is right or wrong, the model presents it with authority. This is the sycophancy dynamic from §4 of the Field Guide — "RLHF prioritizes coherence and confidence over factuality."

**3. Now ground it in the actual paper:**

```
/clear
```

```
Read assets/attention-paper.pdf
```

```
What was the BLEU score achieved by the Transformer base model on the WMT 2014 English-to-German translation task?
```

**WHAT TO EXPECT:** Claude extracts the exact number from the paper (27.3 BLEU) and can point to where it found it. The answer is grounded in source material, not parametric memory.

**4. Push back to test grounding strength:**

```
Are you sure? I thought it was 29.1 BLEU. Can you double-check?
```

**WHAT TO EXPECT:** The grounded model resists the pushback — it has the paper right there and can re-confirm from the source. An ungrounded model is more likely to waver or agree with your (incorrect) suggestion.

> **INSTRUCTOR NOTE:** This is the double lesson: (1) Grounding in sources produces more accurate answers (Rule 4), and (2) Grounded models resist social pressure better because they have evidence to reference (Rule 7). Ungrounded confidence + user pushback = the sycophancy trap.

**KEY TAKEAWAY:** When you have the source, use it. `Read <file>` then ask is always better than asking from memory. And when you get an answer — ground or not — push back to test it. Rule 4 (ground in sources) and Rule 7 (push back on confidence) work together.

---

## Demo 5: The Playbook in Practice (~8 min)

**Playbook rules demonstrated:** All 7 rules
**Concept:** Rapid-fire walkthrough showing how each Playbook rule maps to a concrete Claude Code action.

### Steps

> **INSTRUCTOR NOTE:** This demo is fast-paced. You're connecting the theoretical rules to practical muscle memory. Don't linger on any single example — the goal is pattern recognition.

**Rule 1 — Keep Context Lean and Intentional**

```
/clear
```

Describe verbally the difference between a targeted read and a broad one:

> "In a real project, you'd run `Read src/billing/tax.py` — one specific file. Compare that to asking Claude to 'read every file in this project.' A 500-file codebase could mean 200K+ tokens — your entire context window consumed by files you don't need. Lean context means reading only what you need."

> **INSTRUCTOR NOTE:** This is a verbal example — don't execute the `Read` command here since `src/billing/tax.py` doesn't exist in this demo repo. The point is the *pattern*: targeted reads vs. "read everything."

---

**Rule 2 — Front-Load What Matters**

Show the question-first prompt structure:

```
I need to find the function that calculates sales tax for international orders. It should handle VAT for EU countries. Where is it?

For context, this is a Python e-commerce application using the following structure:
- src/billing/ — invoicing and tax logic
- src/orders/ — order management
- src/shipping/ — fulfillment
```

> **INSTRUCTOR NOTE:** Point out the structure: *question first, then context.* Not "Here's my codebase structure... [long description] ... oh and by the way, where's the tax function?" The model sees the question immediately, then uses the context to answer it.

---

**Rule 3 — Start a New Chat for a New Task**

```
/clear
```

> **INSTRUCTOR NOTE:** "We've been doing this all session. Every time we switch demos, we `/clear`. That's not just housekeeping — it's context hygiene. In your daily work, when you finish a task and start something new, `/clear` or open a new terminal. Your future self will thank you."

---

**Rule 4 — Ground the Model in Source Material**

> **INSTRUCTOR NOTE:** "We already proved this in Demo 4. The pattern is simple: `Read <file>`, then ask. Every time you have the source available, feed it to the model. Don't make it guess from memory."

---

**Rule 5 — Watch for Extrinsic Additions**

```
/clear
```

```
Read demos/ctx-engineering-principles-claude-code/context-window-guide.md
```

```
Summarize section §2 on Context Rot. Only include claims that are explicitly stated in the text. Do not add any information from outside this document.
```

**WHAT TO EXPECT:** Claude produces a tight summary grounded in the document. Compare this to what would happen without the constraint — the model might add its own knowledge about context windows, cite papers not in the document, or elaborate beyond what the text states.

> **INSTRUCTOR NOTE:** "That constraint — 'only include claims explicitly stated in the text' — is Rule 5 in action. It tells the model to extract, not embellish. Without it, you get extrinsic hallucination — plausible additions that aren't in your source."

---

**Rule 6 — Use Structure to Reduce Ambiguity**

```
Based on that same document, create a numbered list of the three mechanisms that drive context rot. For each mechanism, include:
1. The mechanism name
2. A one-sentence definition in your own words
3. A direct quote from the document supporting the definition
```

**WHAT TO EXPECT:** A structured, verifiable output. Each claim is tied to a quote, making it easy to fact-check.

> **INSTRUCTOR NOTE:** "Structured output does two things: it forces the model to organize its reasoning, and it gives you verifiable anchors. Every claim has a quote you can check. This is Rule 6 — use structure to reduce ambiguity."

---

**Rule 7 — Push Back on Confident Answers**

```
What assumptions did you make in creating that summary? What might you have gotten wrong?
```

**WHAT TO EXPECT:** Claude identifies potential weaknesses in its own output — paraphrasing that may have shifted meaning, possible misinterpretation, or areas where the source was ambiguous.

> **INSTRUCTOR NOTE:** "This is the simplest and most powerful habit: after getting an answer, ask 'what did you assume?' or 'what could be wrong?' A model that hallucinated confidently will often reveal its uncertainty under this gentle pressure. That's Rule 7."

---

**Bonus —** CLAUDE.md **as** Persistent **Context Engineering**

```
/clear
```

```
What instructions from CLAUDE.md are currently in your context?
```

> **INSTRUCTOR NOTE:** "CLAUDE.md is static context engineering — instructions that get front-loaded into every session automatically. It's Rule 1 (intentional context) + Rule 2 (front-loaded) applied as infrastructure. In Session 4, we'll go deep on static context files as a production pattern."

**KEY TAKEAWAY:** Every Playbook rule has a concrete Claude Code implementation. Context engineering is not abstract theory — it's specific actions you take every time you interact with a model.

---

## Quick Reference Card

### Playbook Rule → Claude Code Implementation


| #   | Playbook Rule                     | Claude Code Action                                      | Demo      |
| --- | --------------------------------- | ------------------------------------------------------- | --------- |
| 1   | Keep Context Lean                 | `Read <specific-file>` — not "read everything"          | Demo 1, 5 |
| 2   | Front-Load What Matters           | Question first, then context; key info at top of prompt | Demo 3, 5 |
| 3   | New Chat for New Task             | `/clear` between unrelated tasks                        | Demo 2, 5 |
| 4   | Ground in Source Material         | `Read <file>` then ask — don't rely on memory           | Demo 4, 5 |
| 5   | Watch for Extrinsic Additions     | "Only include claims explicitly stated in the text"     | Demo 5    |
| 6   | Use Structure to Reduce Ambiguity | Request numbered lists, quotes, citations               | Demo 5    |
| 7   | Push Back on Confidence           | "What assumptions did you make?"                        | Demo 4, 5 |


### Key Claude Code Commands for Context Management


| Command       | What It Does                                        | When to Use                                                        |
| ------------- | --------------------------------------------------- | ------------------------------------------------------------------ |
| `/context`    | Shows what's currently loaded in the context window | Understand context composition, diagnose bloat                     |
| `/cost`       | Shows token usage for current session               | Monitor context accumulation                                       |
| `/clear`      | Resets conversation context                         | Between unrelated tasks, when context is polluted                  |
| `Read <path>` | Loads a file into context                           | Grounding the model in source material                             |
| `CLAUDE.md`   | Auto-loaded instructions at session start           | Persistent rules, project conventions, front-loaded context        |
| Sub-agents    | Isolated context for sub-tasks                      | Complex tasks where context isolation prevents cross-contamination |


---

*This guide accompanies the [Context Window Field Guide](context-window-guide.md). Both documents are designed for the O'Reilly Live Training: Context Engineering Hands-On, Session 1.*