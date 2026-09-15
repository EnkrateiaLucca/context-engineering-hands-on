# Python Files Summary

- **tools.py** – Defines sandboxed, shell-backed tools (`find_files`, `read_file`, `grep_files`, `write_file`) as Anthropic tool schemas, with `execute_tool` dispatching to safe `find`/`sed`/`grep` calls restricted to a fixed working directory (`_safe_path` blocks path escapes).
- **agent.py** – Implements an `Agent` class that wraps the Anthropic API in a tool-use loop (`run_turn`): sends messages, executes any requested tools via `tools.py`, feeds results back, and repeats until a final text answer or a max round limit is hit.
- **app.py** – A minimal terminal chat REPL around `Agent`, supporting commands (`/help`, `/files`, `/clear`, `/history`, `/quit`) and `@path` syntax to inline file contents into a prompt, with tab-completion for file paths.
