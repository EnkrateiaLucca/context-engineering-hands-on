#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic>=0.115.0", "python-dotenv"]
# ///
"""
SLIDES 2 + 4: the "prompt" is not what the model sees. The model sees ONE flat
token list assembled from several slots. Same question, different context,
different answer.

Run:  uv run 01_what_the_model_sees.py
"""
import json
from _common import ask, count, text

QUESTION = "How many vacation days do I get, and how many roll over?"

# --- Call A: bare question, no context -------------------------------------
msgs_a = [{"role": "user", "content": QUESTION}]
print("A) bare question")
print("   tokens:", count(msgs_a))
print("   answer:", text(ask(msgs_a))[:200], "\n")

# --- Call B: same question, with a system prompt + injected document --------
system = "You are Acme's HR assistant. Answer only from the provided policy. If it is not there, say so."
policy = open("../assets/knowledge-base.md").read()
msgs_b = [{"role": "user", "content": f"<policy>\n{policy}\n</policy>\n\n{QUESTION}"}]
print("B) question + system prompt + policy doc")
print("   tokens:", count(msgs_b, system=system))
print("   answer:", text(ask(msgs_b, system=system))[:200], "\n")

# --- Call C: add history and a tool definition; watch the token count -------
tools = [{
    "name": "search_tickets",
    "description": "Search the IT ticket system by free-text query.",
    "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
}]
history = [
    {"role": "user", "content": "Hi, I'm a backend engineer who started last month."},
    {"role": "assistant", "content": "Welcome! How can I help?"},
]
msgs_c = history + msgs_b
print("C) + 2 turns of history + 1 tool definition")
print("   tokens:", count(msgs_c, system=system, tools=tools))

# --- The point: this is the literal payload. Every slot is just tokens. -----
print("\nWhat the API receives (slots flattened into one request):")
print(json.dumps({"system": system[:60] + "...", "tools": [t["name"] for t in tools],
                  "messages": [{"role": m["role"], "chars": len(m["content"])} for m in msgs_c]}, indent=2))
