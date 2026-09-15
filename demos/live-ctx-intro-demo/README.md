# Live intro: Context Engineering basics

Ten-slide primer plus four runnable demos.

```
slides/intro-context-engineering.html   open in a browser (remark.js, P for presenter notes)
code/01_what_the_model_sees.py           the "prompt" is one flat token list built from slots
code/02_context_budget.py                needle-in-a-haystack: tokens, latency, accuracy vs filler
code/03_four_moves.py                    Write / Select / Compress / Isolate, minimal versions
code/04_agent_loop_growth.py             per-turn token growth in a tool loop, raw vs trimmed
assets/knowledge-base.md                 toy policy doc used by demos 1 and 3
```

Run from `code/` with `ANTHROPIC_API_KEY` set:

```sh
cd code && uv run 01_what_the_model_sees.py
```
