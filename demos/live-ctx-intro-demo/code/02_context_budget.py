#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic>=0.115.0", "python-dotenv"]
# ///
"""
SLIDES 5 + 6: the context window is a budget, and noise costs more than tokens.
Needle-in-a-haystack: same fact, same question, growing filler. Watch tokens,
latency and (often) accuracy move.

Run:  uv run 02_context_budget.py
"""
import random
import time
from _common import ask, count, text

random.seed(0)
NEEDLE = "The deploy freeze exception code for 2026 is ZEBRA-4471."
QUESTION = "What is the deploy freeze exception code for 2026? Reply with the code only."

WORDS = "quarterly roadmap alignment stakeholder synergy pipeline throughput latency budget headcount migration".split()


def filler(n_words: int) -> str:
    return " ".join(random.choice(WORDS) for _ in range(n_words))


def haystack(n_words: int) -> str:
    # ponytail: needle buried at 40% depth; try 0%/100% too, position matters
    before, after = filler(int(n_words * 0.4)), filler(int(n_words * 0.6))
    return f"{before}\n{NEEDLE}\n{after}"


if __name__ == "__main__":
    print(f"{'filler words':>13} {'tokens':>8} {'seconds':>8}  answer")
    for n in [0, 2_000, 10_000, 40_000]:
        msgs = [{"role": "user", "content": f"<notes>\n{haystack(n)}\n</notes>\n\n{QUESTION}"}]
        t0 = time.time()
        resp = ask(msgs, max_tokens=30)
        dt = time.time() - t0
        ok = "OK " if "ZEBRA-4471" in text(resp) else "MISS"
        print(f"{n:>13,} {count(msgs):>8,} {dt:>8.1f}  {ok} {text(resp).strip()[:40]}")

    print("\nTakeaway: every token you load competes for attention and costs money and time.")
    print("200k is a budget, not a feature.")
