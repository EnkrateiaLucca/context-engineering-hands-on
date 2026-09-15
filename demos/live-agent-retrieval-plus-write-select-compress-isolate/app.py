# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "anthropic>=1.6.0",
# ]
# ///
"""
Minimal terminal chat for Agent. Type a message, get a reply.

Commands:  /help  /files  /clear  /history  /quit
Files:     mention @path/to/file to inline its contents into the message.
"""

import re
import readline
from pathlib import Path

from agent import Agent

HELP = """\
/help      show this message
/files     list files in the current folder
/clear     start a fresh session (forget history)
/history   print the conversation so far
/quit      exit
@file.py   inline a file's contents into your message (tab-free: type the path)
"""

AT_TOKEN = re.compile(r"@(\S+)")


def list_files() -> list[str]:
    return sorted(
        str(p) for p in Path(".").rglob("*")
        if p.is_file() and not any(part.startswith(".") for part in p.parts)
    )


def expand_at_files(text: str) -> str:
    """Replace every @path with the file's contents in a fenced block."""
    def sub(m: re.Match) -> str:
        p = Path(m.group(1))
        if not p.is_file():
            print(f"(no such file: {p})")
            return m.group(0)
        return f"\n<file path=\"{p}\">\n{p.read_text()}\n</file>\n"
    return AT_TOKEN.sub(sub, text)


def at_completer(text: str, state: int) -> str | None:
    """Tab-complete @paths against files in the current folder."""
    if not text.startswith("@"):
        return None
    matches = [f"@{f}" for f in list_files() if f.startswith(text[1:])]
    return matches[state] if state < len(matches) else None


def main() -> None:
    readline.set_completer(at_completer)
    readline.set_completer_delims(" \t\n")  # keep '@' and '/' inside the word
    readline.parse_and_bind("bind ^I rl_complete" if "libedit" in readline.__doc__ else "tab: complete")
    agent = Agent()
    print("chat with your agent. /help for commands, /quit to exit.\n")
    while True:
        try:
            text = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text:
            continue
        if text in ("/quit", "/exit", "/q"):
            break
        if text == "/help":
            print(HELP)
        elif text == "/files":
            print("\n".join(list_files()))
        elif text == "/clear":
            agent = Agent()
            print("(session cleared)")
        elif text == "/history":
            for m in agent.messages:
                c = m["content"]
                if isinstance(c, str):
                    print(f"{m['role']}: {c}")
                else:
                    print(f"{m['role']}: [{len(c)} block(s)]")
        elif text.startswith("/"):
            print(f"unknown command: {text}. /help for the list.")
        else:
            print(f"agent> {agent.run_turn(expand_at_files(text))}\n")


if __name__ == "__main__":
    main()
