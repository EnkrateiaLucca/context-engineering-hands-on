# Creating Interactive Webpages from Cheatsheets

How to turn a static reference document into a research-backed interactive guide — without a build system, without a framework, and without leaving your editor.

This is a walkthrough of the process used to build `context-window-guide.html` from `context-window-guide.md`.

---

## The Starting Point

The input was a well-structured markdown file: 8 sections, citations, tables, callouts. Useful as a reference, but static — every concept was described in prose, every data point was mentioned in a sentence, and nothing invited interaction.

The transformation goal: make the research tangible. Not just tell someone that "performance drops 30% in the middle" but let them *see* the U-curve and click through it.

---

## Phase 1: Research the Sources Before You Build

The single most important step happens before any code is written.

The markdown file contained 8 source citations. Most people would build the page using only what the markdown already said. Instead, **go back to the original papers and articles and extract quantitative data**.

### Why This Matters

A markdown cheatsheet necessarily flattens research into prose summaries. The actual papers contain tables with exact accuracy numbers at every position, performance curves across token lengths, and comparison data across multiple models — all of it suitable for interactive charts.

### What to Look For

For each source, extract:
- **Exact numbers** — percentages, token counts, accuracy figures
- **Comparison data** — model A vs. model B, condition X vs. condition Y
- **Breakdowns by variable** — accuracy by position, performance by context length
- **Thresholds and inflection points** — where does performance start degrading? What's the crossover point?

### What This Found

From Liu et al. (Lost in the Middle, TACL 2024) — the paper contains full tables:

```
Multi-Document QA, 20 documents, GPT-3.5-Turbo:
  Position 0  → 75.8% accuracy
  Position 4  → 57.2%
  Position 9  → 53.8%   ← middle
  Position 14 → 55.4%
  Position 19 → 63.2%   ← end
  Closed-book baseline: 56.1%
```

That last line is the critical finding: at positions 4 through 14, GPT-3.5's performance **falls below what it achieves with no context at all**. Adding more documents actively hurts. You can't communicate that with a sentence — you need a chart with a baseline line.

From the Adobe multi-hop NIAH study (retrieved via Understanding AI):

```
GPT-4o:          99% → 70%  at 32K tokens  (-29pp)
Claude 3.5:      88% → 30%  at 32K tokens  (-58pp)
Gemini 2.5 Flash: 94% → 48%  at 32K tokens  (-46pp)
Llama 4 Scout:   82% → 22%  at 32K tokens  (-60pp)
```

From Chroma Research (context rot study):

```
Pairwise attention relationships:
  10K tokens  → 100 million
  100K tokens → 10 billion
  1M tokens   → 1 trillion
```

This is the data that powers the visualizations. Without this research step, you'd be building decorative charts with made-up values.

---

## Phase 2: Audit the Existing HTML

The markdown file had an existing HTML companion (`context-window-guide.html`) — a solid static page with good design. Before rewriting anything, read the full file to understand:

- What design tokens exist (colors, fonts, spacing)
- What components are already built (cards, callouts, tables)
- What CSS variables are established
- What can be kept vs. what needs to change

**Key principle: preserve the design system.** The brand tokens (`--coral`, `--golden`, `--sage`, `--sky`, etc.), the typography stack (IBM Plex Sans + JetBrains Mono), and the black-border card aesthetic were all worth keeping. The transformation was additive, not a replacement.

---

## Phase 3: Map Concepts to Interactive Elements

For each section of the document, ask: *what's the most natural way to make this tangible?*

| Concept | Static form | Interactive form |
|---|---|---|
| Token count basics | A prose explanation | A live calculator with fill bar |
| Attention dilution | "More tokens = exponentially more relationships" | Log-scale bar chart with tooltips showing exact relationship counts |
| Performance drop at 32K | A sentence with percentages | Grouped bar chart: baseline vs. 32K, hover for pp drop |
| Lost in the Middle U-curve | A summary statement | Multi-model line chart, switchable between 10/20/30 docs |
| Position impact | An explanation of the effect | Clickable position strip showing exact accuracy per position |
| Hallucination types | Four type descriptions | Accordion cards with examples + detection strategies |
| Playbook rules | A numbered list | Checkable rules with progress bar |
| Trust conditions | A bulleted list | Three-state conditions (met/unmet/unchecked) with live trust score |

### Decision Rule

Add interactivity only where it does one of two things:
1. **Reveals data that can't be communicated in prose** (charts with multiple data series, exact values at specific positions)
2. **Asks the reader to engage with their own situation** (calculator, self-assessment)

Don't add interactivity for its own sake. Hover effects on the quick-reference cards (already in the static page) are sufficient — they don't need to become tabs or modals.

---

## Phase 4: Choose the Right Tools

For a single-file HTML guide with no build process:

**Charts: Chart.js via CDN**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

Chart.js is the right call here because:
- Single CDN import, no npm, no bundler
- Handles line, bar, and mixed charts natively
- Tooltips are customizable with `callbacks`
- Responsive by default with `maintainAspectRatio: false`

Alternatives like D3 would give more control but require significantly more code for standard chart types. For a reference guide, Chart.js is the better tradeoff.

**Everything else: vanilla JS**

Token calculator, accordion toggles, progress tracking, filter buttons, IntersectionObserver for nav state — all of this is straightforward DOM manipulation that doesn't need a library.

---

## Phase 5: Build the Charts

### The U-Curve Chart

The key to making the U-curve useful is the **closed-book baseline annotation**:

```js
{
  label: 'Closed-book baseline (GPT-3.5)',
  data: d.labels.map(() => d.baseline),  // flat line at 56.1
  borderColor: '#F5C542',
  borderDash: [6, 4],
  pointRadius: 0,
}
```

And the tooltip callback that flags when performance dips below it:

```js
tooltip: {
  callbacks: {
    footer: (items) => {
      const gptVal = items.find(i => i.dataset.label === 'GPT-3.5-Turbo');
      if (gptVal && gptVal.raw < d.baseline) {
        return ['⚠ Below closed-book baseline — context is hurting'];
      }
      return [];
    }
  }
}
```

This makes the counterintuitive finding (more context = worse than no context) surfaceable on hover, not buried in footnotes.

### The Document Count Switcher

The chart supports 10, 20, and 30 documents by storing all data upfront and rebuilding the chart on button click:

```js
const docsData = {
  10: { labels: ['0','4','9'], gpt35: [...], ... },
  20: { labels: ['0','4','9','14','19'], gpt35: [...], ... },
  30: { labels: ['0','4','9','14','19','24','29'], gpt35: [...], ... },
};

function setDocs(n, btn) {
  // destroy and rebuild the chart with new data
  if (uCurveChart) uCurveChart.destroy();
  buildUCurve(n);
}
```

Chart.js requires destroying the old instance before creating a new one on the same canvas element.

### The Attention Dilution Chart

Logarithmic scale is essential here — the relationship counts span 7 orders of magnitude (100M to 1T). Without log scale, the 10K bar would be invisible:

```js
scales: {
  y: {
    type: 'logarithmic',
    ticks: {
      callback: (v) => {
        const map = { 100: '100M', 10000: '10B', 1000000: '1T' };
        return map[v] || '';
      }
    }
  }
}
```

---

## Phase 6: Build the Interactive Components

### Token Calculator

Token estimation is approximate — the common approximation is 75 words ≈ 100 tokens:

```js
function estimateTokens(text) {
  const words = text.trim().split(/\s+/).filter(w => w.length > 0);
  return Math.round(words.length * (100 / 75));
}
```

The fill bar gives immediate visual feedback by changing color as utilization increases:

```js
tokenFill.className = 'token-context-fill';
if (pct > 75) tokenFill.classList.add('danger');     // → red
else if (pct > 40) tokenFill.classList.add('warning'); // → yellow
// else stays green
```

### Position Simulator

Pre-compute all 20 positions with accuracy, label, and attention tier. The accuracy values interpolate between the known data points from the Liu et al. paper:

```js
const positionData20 = {
  0:  { acc: 75.8, label: 'Start of context', attention: 'high' },
  9:  { acc: 53.8, label: 'Dead middle — lowest accuracy', attention: 'low' },
  19: { acc: 63.2, label: 'End of context', attention: 'high' },
  // ...
};
```

Color the strip segments by attention tier using CSS classes — blue tint for high attention zones, muted for low:

```css
.context-chunk.high-attention { background: var(--sky-light); border-color: var(--sky); }
.context-chunk.low-attention  { background: var(--gray-100); }
```

### Accordion Pattern for Hallucination Types

A single `toggleType` function handles all four type cards. The toggle reads the sibling relationship between the header and the body:

```js
function toggleType(header) {
  const body = header.nextElementSibling;
  const toggle = header.querySelector('.type-toggle');
  body.classList.toggle('open');
  toggle.style.transform = body.classList.contains('open') ? 'rotate(45deg)' : '';
}
```

CSS does the rest — `display: none` / `display: block` on `.type-body` with `.open` applied.

### Three-State Trust Assessment

The trust score cycles through three states on each click: unchecked → met → unmet → unchecked. This models the real situation — some conditions you haven't assessed, some you know are met, some you know are not:

```js
function toggleCond(id) {
  if (condStates[id] === 'met')    condStates[id] = 'unmet';
  else if (condStates[id] === 'unmet') condStates[id] = null;
  else                             condStates[id] = 'met';
  // update score...
}
```

---

## Phase 7: Navigation

The sticky nav uses the IntersectionObserver API to track which section is visible and highlight the corresponding nav link:

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navLinks.forEach(a => a.classList.remove('active'));
      navLinks.forEach(a => {
        if (a.dataset.section === entry.target.id) a.classList.add('active');
      });
    }
  });
}, { threshold: 0.3, rootMargin: '-50px 0px -50% 0px' });
```

The `rootMargin` shrinks the detection zone from the bottom, so the active section updates before the user has fully scrolled past it.

For smooth scroll-to-section on click, a single CSS declaration handles it:

```css
html { scroll-behavior: smooth; }
```

Combined with `scroll-margin-top` on each section to account for the sticky nav height:

```css
.section {
  scroll-margin-top: calc(var(--nav-h) + 16px);
}
```

---

## The Resulting Structure

```
context-window-guide.html
├── <style>          Brand tokens + component CSS (~400 lines)
├── Sticky nav       IntersectionObserver-driven active state
├── Header           Key stats from the research as stat pills
├── Quick reference  Clickable cards → scroll to sections
├── §1               Token calculator (live, with fill bar)
├── §2               Attention chart + performance drop chart
├── §3               U-curve chart + position simulator
├── §4               Hallucination type accordion
├── §5               Static (concept doesn't need interactivity)
├── §6               Interactive playbook checklist + progress bar
├── §7               Filterable trust calibration table
├── §8               Trust score self-assessment (3-state)
└── <script>         All interaction logic (~200 lines, vanilla JS)
```

Total: ~1,000 lines. No build step. No dependencies beyond a Chart.js CDN import.

---

## Principles That Generalize

**1. Research before building.** The source document is a summary. Go back to the originals and extract the tables and numbers the summary had to flatten.

**2. Map concepts to their natural interaction.** Comparisons → charts. Personal applicability → self-assessment. Multi-dimensional data → toggles or filters. Don't force a concept into an interaction type that doesn't fit.

**3. Preserve the existing design system.** If there's an existing CSS token system, use it. The visual coherence is worth more than starting from scratch.

**4. Annotations carry the insight.** Charts without annotations are decoration. The closed-book baseline line, the tooltip that says "⚠ context is hurting here," the color change on the fill bar — these are the things that make the data communicate.

**5. Keep the file portable.** A single HTML file that opens from disk and works offline is more durable than a deployed web app. CDN dependencies are a reasonable exception for visualization libraries.
