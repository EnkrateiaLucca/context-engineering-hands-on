# /// script
# requires-python = ">=3.11"
# dependencies = ["reportlab>=4.0"]
# ///
"""
Generate the Context Engineering Tools & Patterns cheatsheet PDF.

This is the SOURCE for assets/context-engineering-tools-cheatsheet.pdf — the
printable reference handed out with the course. Edit the content here and
regenerate so the PDF never drifts from the slide decks.

Run:
    uv run scripts/generate_cheatsheet.py
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent.parent / "assets" / "context-engineering-tools-cheatsheet.pdf"

# ---- Palette (shared with the slide decks) ----------------------------------
BG = HexColor("#f5f0e6")
INK = HexColor("#1a1a1a")
BODY = HexColor("#333333")
GOLD = HexColor("#d9a441")
AMBER = HexColor("#e7c548")
RED = HexColor("#e26b5a")
BLUE = HexColor("#66a3d2")

CALLOUTS = {
    "CAUTION": (HexColor("#fbf3da"), AMBER),
    "ALERT": (HexColor("#fbe4e0"), RED),
    "INFORMATION": (HexColor("#e6f0fb"), BLUE),
}

# ---- Styles -----------------------------------------------------------------
title = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=24,
                       leading=28, textColor=INK, alignment=TA_CENTER)
subtitle = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=10,
                          leading=14, textColor=BODY)
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=17, leading=20,
                    textColor=INK, spaceBefore=20, spaceAfter=6)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13, leading=16,
                    textColor=INK, spaceBefore=12, spaceAfter=3)
body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=13,
                      textColor=BODY, spaceAfter=4)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=10, firstLineIndent=-10)
label = ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=7.5,
                       leading=10, textColor=HexColor("#666666"))
callout_body = ParagraphStyle("callout_body", parent=body, spaceBefore=4, spaceAfter=0)
foot = ParagraphStyle("foot", fontName="Helvetica-Oblique", fontSize=9,
                      leading=12, textColor=BODY, alignment=TA_LEFT)

FRAME_W = letter[0] - 108  # 54pt margins each side


# ---- Helpers ----------------------------------------------------------------
def H1(text):
    return Paragraph(text, h1)


def H2(text):
    return Paragraph(text, h2)


def P(text, style=body):
    return Paragraph(text, style)


def B(text):
    return Paragraph(f"• {text}", bullet)


def N(num, text):
    return Paragraph(f"{num}. {text}", bullet)


def callout(kind, text):
    bg, border = CALLOUTS[kind]
    inner = [Paragraph(kind, label), Paragraph(text, callout_body)]
    t = Table([[inner]], colWidths=[FRAME_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEABOVE", (0, 0), (-1, 0), 3, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    return t


def draw_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, letter[0], letter[1], stroke=0, fill=1)
    canvas.restoreState()


# ---- Content ----------------------------------------------------------------
def story():
    s = []
    s.append(Spacer(1, 24))
    s.append(P("Context Engineering Tools &amp; Patterns Cheatsheet", title))
    s.append(HRFlowable(width=90, thickness=3, color=GOLD,
                        spaceBefore=8, spaceAfter=16, hAlign="CENTER"))
    s.append(P("<b>Hands-On Context Engineering</b> — O'Reilly Live Training · Lucas Soares", subtitle))
    s.append(Spacer(1, 6))
    s.append(callout("CAUTION",
        "<b>Context engineering</b> is the discipline of designing the architecture that feeds an "
        "LLM the <b>right information</b> at the <b>right time</b>. It transforms high-entropy human "
        "intentions into low-entropy representations machines can process. Unlike humans, machines "
        "cannot “fill in the gaps.”"))

    s.append(H1("The Four Context Operations (W/S/C/I)"))
    s.append(P("Every context engineering strategy maps to one of these four fundamental operations."))
    s.append(B("<b>WRITE</b> — Create context that doesn't exist yet. Plans, instructions, scratchpads, "
               "learned knowledge, memories. Agent writes files for future reference."))
    s.append(B("<b>SELECT</b> — Choose the most relevant context from available sources. Semantic search, "
               "structural search (grep/glob), adaptive retrieval, dynamic tool loading, skills."))
    s.append(B("<b>COMPRESS</b> — Reduce size while preserving essential information. Summarization, pruning, "
               "offloading to disk, spawning subagents for token-heavy ops."))
    s.append(B("<b>ISOLATE</b> — Separate context types to prevent interference. Subagent isolation, dynamic "
               "tool loading, working memory scratchpads, state objects."))

    s.append(H1("The Four Context Failure Modes"))
    s.append(P("Drew Breunig's taxonomy — each mode has distinct symptoms and specific fix levers."))
    s.append(B("<b>POISONING</b> — Hallucination enters context and compounds. Agent treats its own prior "
               "output as ground truth. <i>Signal: bad fact reappears across steps.</i> Fix: <b>Isolate + Select</b>"))
    s.append(B("<b>DISTRACTION</b> — Too much history causes the agent to repeat past behavior instead of "
               "reasoning fresh. <i>Signal: agent repeats prior actions.</i> Fix: <b>Compress + Select</b>"))
    s.append(B("<b>CONFUSION</b> — Irrelevant tools or documents crowd the context, leading to wrong tool "
               "selection. <i>Signal: irrelevant tools/docs selected.</i> Fix: <b>Select + Isolate</b>"))
    s.append(B("<b>CLASH</b> — Contradictory information creates conflicting assumptions and unreliable "
               "output. <i>Signal: flip-flopping between approaches.</i> Fix: <b>Isolate + Select</b>"))

    s.append(H1("Quick Reference: Failures to Fixes"))
    s.append(B("<b>Poisoning</b> → Primary: Isolate + Select | Supporting: Write (claims + sources) | "
               "Prune hallucinated turns, add validation instructions"))
    s.append(B("<b>Distraction</b> → Primary: Compress + Select | Supporting: Write (persistent plan) | "
               "Summarize stale history, select smaller working set"))
    s.append(B("<b>Confusion</b> → Primary: Select + Isolate | Supporting: Tool Loadout (dynamic) | "
               "Load only relevant tools per step, isolate nice-to-have context"))
    s.append(B("<b>Clash</b> → Primary: Isolate + Select | Supporting: Compress (resolved summary) | "
               "Quarantine tasks into separate contexts, set precedence rules"))

    s.append(H1("The Five-Step Debugging Loop"))
    s.append(N(1, "<b>Inspect Trace</b> — Walk through messages, tool calls, and outputs turn by turn"))
    s.append(N(2, "<b>Tag Failure</b> — Which mode? Poisoning / Distraction / Confusion / Clash"))
    s.append(N(3, "<b>Pick a Lever</b> — Use the Write / Select / Compress / Isolate framework"))
    s.append(N(4, "<b>Re-run &amp; Evaluate</b> — Track token usage per step AND measure outcome quality"))
    s.append(N(5, "<b>Iterate</b> — Context engineering is iterative, not one-shot"))
    s.append(Spacer(1, 6))
    s.append(callout("ALERT",
        "Don't just optimize for fewer tokens — <b>measure outcome quality</b>. A fix that reduces "
        "tokens but degrades results is worse."))

    s.append(H1("Context Budget Problem"))
    s.append(P("Every agent must make critical decisions about its finite context budget:"))
    s.append(B("<b>Keep Active</b> — What stays in the context window right now?"))
    s.append(B("<b>Store Externally</b> — What goes to disk or DB for later?"))
    s.append(B("<b>Compress</b> — What can be summarized to save space?"))
    s.append(B("<b>Reserve</b> — How much capacity for reasoning?"))
    s.append(Spacer(1, 6))
    s.append(callout("CAUTION",
        "<b>Bigger windows are NOT better.</b> Models now support 100K, 200K, even 1M+ tokens — but "
        "performance degrades well before hitting limits. Chroma's “Context Rot” study (2025) found "
        "accuracy dropped <b>20–50% between 10K and 100K tokens</b> across 18 frontier models, hitting "
        "abrupt “cliffs” rather than declining gradually. Published context window ≠ usable context window."))

    s.append(H1("Context Prioritization Hierarchy"))
    s.append(B("<b>CRITICAL</b> (always include): Current code/content being modified, specific error messages, "
               "expected output format, active task requirements"))
    s.append(B("<b>HELPFUL</b> (include if space permits): Project structure, dependencies in use, coding "
               "conventions, related documentation"))
    s.append(B("<b>OPTIONAL</b> (include only if needed): Historical decisions, future plans, tangential "
               "examples, background reference"))

    s.append(H1("Production Patterns from Real Systems"))
    s.append(H2("The Static-to-Dynamic Spectrum"))
    s.append(B("<b>Static</b> — Always loaded (CLAUDE.md, .cursorrules). Predictable but stale, always-costing tokens."))
    s.append(B("<b>Tiered</b> — Hot/warm/cold layers loaded by role or trigger. Structured, requires infrastructure."))
    s.append(B("<b>Dynamic</b> — Agent discovers and fetches on demand (Cursor, Claude Code grep/glob, Agent "
               "Skills). Token-efficient, always fresh."))
    s.append(B("<b>Self-Improving</b> — Contexts evolve based on execution feedback (ACE framework). No manual maintenance."))

    s.append(H2("Manus's 5 Production Strategies"))
    s.append(N(1, "<b>Context Compaction &amp; Summarization</b> — Reversible compaction (store file paths, "
               "not contents) + lossy summarization triggered at ~128K tokens"))
    s.append(N(2, "<b>Communication Over Shared Context</b> — Fresh sub-agents for discrete tasks instead of "
               "sharing full conversation history"))
    s.append(N(3, "<b>Hierarchical Action Spaces</b> — Limit visible tools to ~20 atomic tools. Level 2: "
               "sandbox utilities. Level 3: code libraries"))
    s.append(N(4, "<b>Agent-as-Tool Pattern</b> — Sub-agents as deterministic functions with defined inputs, "
               "outputs, and JSON schemas"))
    s.append(N(5, "<b>Implementation Best Practices</b> — Avoid dynamic RAG-based tool retrieval (breaks KV "
               "cache). Set pre-rot thresholds at 70-80% utilization"))

    s.append(H2("Static Context Files: The ETH Zurich Study"))
    s.append(B("<b>-3% success rate</b>: LLM-generated context files actually hurt performance"))
    s.append(B("<b>+4% success rate</b>: Human-written context files give marginal improvement"))
    s.append(B("<b>+20% cost increase</b> across both file types (14-22% more reasoning tokens)"))
    s.append(B("<b>Best practice</b>: Keep it minimal (10-20 lines), specific tooling only, don't duplicate "
               "README content, review quarterly"))

    s.append(H2("Key Retrieval Approaches"))
    s.append(B("<b>Vector Store (RAG)</b> — Classic chunking + embeddings + similarity search. Requires "
               "indexing, chunking decisions."))
    s.append(B("<b>Agentic Search</b> — llm.txt file with URLs + descriptions. Agent fetches docs on demand. "
               "Extremely effective with good descriptions."))
    s.append(B("<b>Context Stuffing</b> — Feed all docs directly to the agent. Brute force. Expensive and "
               "degrades quality."))
    s.append(B("<b>Progressive Disclosure</b> — Start small, expand as needed. Don't pre-load everything. "
               "File paths and links — load full content only when needed."))

    s.append(H2("Agent Skills: Progressive Disclosure as a Primitive"))
    s.append(P("A skill is a folder — a SKILL.md file plus optional scripts — the agent loads only when "
               "the task needs it. Progressive disclosure, packaged."))
    s.append(B("<b>At startup</b> — only the skill's name + one-line description (~30–80 tokens) sit in context."))
    s.append(B("<b>On trigger</b> — the full SKILL.md body loads; bundled scripts run without ever entering the window."))
    s.append(B("<b>Why it matters</b> — the Select lever, productized: instructions load just-in-time instead "
               "of always-on. Contrast CLAUDE.md (always-on) with a skill (load-on-demand)."))
    s.append(B("<b>Open standard</b> (Dec 2025) — the SKILL.md format is portable across Claude Code, Cursor, "
               "and 25+ other platforms."))

    s.append(H2("The Compression Toolkit"))
    s.append(B("<b>Prompted Summarization</b> — Compress with high recall. Exhaustive bullet points so the "
               "agent knows whether to retrieve full context."))
    s.append(B("<b>Auto-Compaction</b> — Automatic compression nearing limits. Claude Code auto-compacts at 95% capacity."))
    s.append(B("<b>Trimming</b> — Selective removal using heuristics. Keep only recent N messages or LLM-scored relevance."))
    s.append(B("<b>Prompt Caching</b> — Avoid re-sending invariant context. System prompts, tool definitions "
               "— cache, don't reprocess."))
    s.append(B("<b>Context Offloading</b> — Write full results to disk, return summary + pointer to the agent. "
               "Agent fetches on demand."))
    s.append(Spacer(1, 6))
    s.append(callout("ALERT",
        "<b>Risk:</b> Summarization loses information. Always <b>offload to disk before summarizing</b> to "
        "retain raw context as a safety net."))

    s.append(H1("Course Demos Quick Reference"))
    s.append(H2("Demo 1: Context Engineering Principles (Claude Code)"))
    s.append(P("<b>Session 1</b> — Live CLI demos with Claude Code. No code to run — uses claude directly."))
    s.append(B("/context — Make the context window visible (see what the model sees)"))
    s.append(B("/cost — Track token consumption per session"))
    s.append(B("/clear — Reset context to demonstrate context rot recovery"))
    s.append(B("Read tool — Ground the model in documents (beats parametric memory)"))
    s.append(B("CLAUDE.md — Static context file as persistent instructions"))
    s.append(B("Lost in the Middle: Same question, same document — answer quality depends on WHERE the fact is positioned"))

    s.append(H2("Demo 2: Agentic Retrieval (Interactive TUI)"))
    s.append(P("<b>Session 2</b> — Run: uv run app.py in demos/agentic-retrieval/"))
    s.append(B("Hand-rolled agent loop — self.messages IS the context window, made explicit and inspectable"))
    s.append(B("Progressive disclosure retrieval: list_documents (cheap) → search_documents (moderate) "
               "→ get_document (expensive)"))
    s.append(B("System prompt ~200 tokens (WRITE lever), tool definitions ~800 tokens fixed overhead per call"))
    s.append(B("Slash commands: /context shows the live messages array, /stats shows token counts"))
    s.append(B("TF-IDF search with scikit-learn — no vector DB needed for small knowledge bases"))
    s.append(B("Teaching point: every append() to messages is a permanent token cost"))

    s.append(H2("Demo 3: Context Failures (Jupyter Notebook)"))
    s.append(P("<b>Session 3</b> — Open: context_failures.ipynb in demos/context-failures/"))
    s.append(B("<b>Poisoning</b>: Hallucinated “AI Code Review” feature compounds across turns. Fix: prune + validation instruction."))
    s.append(B("<b>Distraction</b>: 5 verbose brute-force turns bias the model away from optimal DP solution. Fix: summarize to one-liner."))
    s.append(B("<b>Confusion</b>: 12 irrelevant tool schemas (~2,400 tokens overhead) for a simple factual question. Fix: remove all tools."))
    s.append(B("<b>Clash</b>: Budget trip plan contradicts later luxury requirements. Fix: prune old plan + add CURRENT REQUIREMENTS override."))
    s.append(B("Each scenario shows broken vs. fixed with real token cost comparison and HTML dashboard"))

    s.append(H2("Demo 4: Chat with Artifacts (Web App)"))
    s.append(P("<b>Session 4</b> — Run: uv run app.py in demos/chat-with-artifacts/ → open http://127.0.0.1:8000"))
    s.append(B("Layered system prompt: Layer 1 (fixed persona ~150 tok) + Layer 2 (static artifact schemas "
               "~400 tok) + Layer 3 (dynamic state 0-200 tok)"))
    s.append(B("7 artifact types: selectable_options, flashcard_deck, checklist, flowchart, semantic_zoom, "
               "inline_quiz, concept_explorer"))
    s.append(B("Structured output via tool_choice — guaranteed JSON matching schema. “The prompt provides "
               "the content; the schema provides the shape.”"))
    s.append(B("ArtifactRegistry injects dynamic context: tracks what's been created, tells model to build on existing artifacts"))
    s.append(B("structured_outputs_demo.py — Same prompt, 3 different schemas, 3 different output shapes. Same input cost."))

    s.append(H1("Key Numbers to Remember"))
    s.append(B("<b>500K tokens</b> per run for naive deep research agents | <b>$1-2</b> cost per single agent run"))
    s.append(B("<b>~50-100</b> tool calls in production agents | <b>83.9%</b> of context consumed by tool outputs"))
    s.append(B("<b>n² attention complexity</b> — more tokens = exponentially more pairwise relationships to score"))
    s.append(B("<b>95% capacity</b> — Claude Code auto-compaction trigger | <b>70-80%</b> — Manus pre-rot threshold"))
    s.append(B("<b>46.9%</b> token reduction from Cursor's dynamic context discovery | <b>44%</b> performance "
               "improvement from dynamic tool loading"))
    s.append(B("<b>~30–80 tokens</b> — Agent Skill discovery cost (name + description) until triggered | "
               "<b>26+ platforms</b> adopting the SKILL.md open standard"))
    s.append(B("<b>~150-200 instructions</b> — frontier LLM instruction-following limit. Claude Code's system "
               "prompt already uses ~50."))

    s.append(H1("Core Principles"))
    s.append(callout("INFORMATION",
        "“Find the smallest set of high-signal tokens that maximize the likelihood of your desired "
        "outcome.” — Anthropic, Effective Context Engineering for AI Agents"))
    s.append(Spacer(1, 6))
    s.append(N(1, "<b>Context engineering is entropy reduction</b> — High-entropy intentions into low-entropy "
               "representations machines understand"))
    s.append(N(2, "<b>Systems, not prompts</b> — The full architecture of information flow: storage, "
               "management, and usage"))
    s.append(N(3, "<b>Four operations: Write, Select, Compress, Isolate</b> — Every strategy maps to one of these"))
    s.append(N(4, "<b>Quality over quantity</b> — Bigger windows don't help. Focused, relevant, well-managed context does."))
    s.append(N(5, "<b>Context hygiene is continuous</b> — Monitor, prune, refresh, and validate throughout the lifecycle"))
    s.append(N(6, "<b>Agentic retrieval beats naive RAG</b> — Simple tools (grep/glob) with progressive "
               "disclosure outperform complex pipelines"))
    s.append(N(7, "<b>Read tasks parallelize, write tasks don't</b> — Sub-agents for research, single-threaded "
               "execution for code generation"))
    s.append(N(8, "<b>Offload before you summarize</b> — Save raw context to disk first, then compress. "
               "Summarization is lossy."))
    s.append(Spacer(1, 14))
    s.append(P("Hands-On Context Engineering — O'Reilly Live Training · Lucas Soares · 2026", foot))
    return s


def main():
    doc = BaseDocTemplate(
        str(OUT), pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=48, bottomMargin=48,
        title="Context Engineering Tools & Patterns Cheatsheet",
        author="Lucas Soares",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="cream", frames=[frame], onPage=draw_bg)])
    doc.build(story())
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
