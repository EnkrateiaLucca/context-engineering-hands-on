#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic>=0.115.0", "python-dotenv"]
# ///
"""
SLIDE 8: nobody designs turn 8's context, it accumulates. A tool-use loop where
the tool returns big blobs. Run once raw, once with a 400-char cap on tool
results, and compare the per-turn token curve.

Run:  uv run 04_agent_loop_growth.py
"""
import json
from _common import ask, count

SYSTEM = "You are a log analyst. Use the tool to read logs. When done, answer in one sentence."
TOOLS = [{
    "name": "read_log",
    "description": "Read a service log file. Available: api.log, db.log, worker.log.",
    "input_schema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
}]
USER = "Which service is throwing errors? Check all three logs, then answer."


def read_log(name: str) -> str:
    # 300 lines of noise, one real error in db.log
    lines = [f"2026-09-15T10:00:{i % 60:02d} INFO {name} request_id=abc{i} status=200 latency=12ms" for i in range(300)]
    if name == "db.log":
        lines[187] = "2026-09-15T10:03:07 ERROR db.log connection pool exhausted (max=50)"
    return "\n".join(lines)


def run(cap: int | None) -> list[int]:
    msgs = [{"role": "user", "content": USER}]
    curve = []
    for turn in range(8):
        curve.append(count(msgs, system=SYSTEM, tools=TOOLS))
        resp = ask(msgs, system=SYSTEM, tools=TOOLS, max_tokens=500)
        msgs.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            break
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                out = read_log(block.input["name"])
                if cap:  # COMPRESS at the source: trim before it enters the window
                    err = [l for l in out.splitlines() if "ERROR" in l]
                    out = "\n".join(err) if err else out[:cap] + f"\n... ({len(out)} chars, no ERROR lines)"
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": out})
        msgs.append({"role": "user", "content": results})
    return curve


if __name__ == "__main__":
    raw = run(cap=None)
    trimmed = run(cap=400)
    print(f"{'turn':>4} {'raw tokens':>11} {'trimmed':>9}")
    for i in range(max(len(raw), len(trimmed))):
        r = raw[i] if i < len(raw) else "-"
        t = trimmed[i] if i < len(trimmed) else "-"
        print(f"{i+1:>4} {r:>11} {t:>9}")
    print("\nSame task, same answer. The only change: the tool trimmed its own output.")
