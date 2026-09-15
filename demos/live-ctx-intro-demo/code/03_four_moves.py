#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic>=0.115.0", "python-dotenv"]
# ///
"""
SLIDE 7: the whole toolkit is four moves. Each function below is the smallest
honest version of one move.

  WRITE     persist outside the window (a memory file)
  SELECT    load only the relevant slice (keyword retrieval over the KB)
  COMPRESS  summarize history before it grows
  ISOLATE   hand a sub-task to a fresh context and keep only the result

Run:  uv run 03_four_moves.py
"""
import os
import re
from _common import ask, count, text

KB = open("../assets/knowledge-base.md").read()
MEMORY_FILE = "/tmp/ctx_demo_memory.md"


# --- WRITE ------------------------------------------------------------------
def write_memory(fact: str) -> None:
    with open(MEMORY_FILE, "a") as f:
        f.write(f"- {fact}\n")


def read_memory() -> str:
    return open(MEMORY_FILE).read() if os.path.exists(MEMORY_FILE) else ""


# --- SELECT -----------------------------------------------------------------
def select(question: str, kb: str = KB, k: int = 2) -> str:
    """Return the k KB sections sharing the most words with the question.
    ponytail: bag-of-words overlap; swap for embeddings when this misses."""
    sections = re.split(r"\n(?=## )", kb)
    q = set(re.findall(r"\w+", question.lower()))
    scored = sorted(sections, key=lambda s: -len(q & set(re.findall(r"\w+", s.lower()))))
    return "\n\n".join(scored[:k])


# --- COMPRESS ---------------------------------------------------------------
def compress(history: list[dict]) -> list[dict]:
    transcript = "\n".join(f"{m['role']}: {m['content']}" for m in history)
    summary = text(ask([{"role": "user", "content":
        f"Summarize this conversation in 2 sentences, keeping every concrete fact:\n\n{transcript}"}]))
    return [{"role": "user", "content": f"[Summary of earlier conversation]\n{summary}"},
            {"role": "assistant", "content": "Understood, continuing from that summary."}]


# --- ISOLATE ----------------------------------------------------------------
def isolate(task: str, context: str) -> str:
    """Run a sub-task in a fresh window. The parent only ever sees the return value."""
    return text(ask([{"role": "user", "content": f"{task}\n\n<context>\n{context}\n</context>"}], max_tokens=150))


if __name__ == "__main__":
    q = "I'm traveling next week. What can I expense for meals and do I need receipts?"

    print("SELECT: full KB =", count([{"role": "user", "content": KB}]), "tokens;",
          "selected =", count([{"role": "user", "content": select(q)}]), "tokens")
    print("   ->", select(q).splitlines()[0])

    write_memory("User is a backend engineer who started last month.")
    write_memory("User travels next week.")
    print("\nWRITE: memory file now holds:\n" + read_memory())

    history = [
        {"role": "user", "content": "I need to plan my trip to the Berlin office."},
        {"role": "assistant", "content": "Sure. When are you going?"},
        {"role": "user", "content": "Next Tuesday to Thursday, flying from Lisbon."},
        {"role": "assistant", "content": "Got it, Lisbon to Berlin, Tue-Thu."},
    ]
    compressed = compress(history)
    print("COMPRESS:", count(history), "->", count(compressed), "tokens")
    print("   ->", compressed[0]["content"][:160])

    verdict = isolate("Does the on-call policy say who is paged first? Answer in one sentence.", KB)
    print("\nISOLATE: sub-task ran with the full KB; parent received only:", len(verdict), "chars")
    print("   ->", verdict.strip())

    # Everything assembled for the final call: memory + selected KB + compressed history
    final = compressed + [{"role": "user", "content": f"<memory>\n{read_memory()}</memory>\n<policy>\n{select(q)}\n</policy>\n\n{q}"}]
    print("\nFINAL call tokens:", count(final))
    print(text(ask(final)))
    os.remove(MEMORY_FILE)
