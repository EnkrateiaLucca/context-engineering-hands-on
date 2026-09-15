import subprocess
from pathlib import Path
from typing import Any

WORKDIR = Path(__file__).parent.resolve()

def get_tool_definitions() -> list[dict]:
    """
    Return tool schemas in Anthropic API format.

    Three shell-backed tools that let the agent explore a working directory:
    - find_files: `find <cwd> -name <pattern>` — locate files by glob
    - read_file:  `sed -n '<start>,<end>p' <path>` — read a file (or a line range)
    - grep_files: `grep -rn <pattern> <cwd>` — search file contents

    All paths are relative to a fixed working directory chosen by the host.
    The executor must resolve every path and reject anything outside that
    root — the model's input is untrusted.

    Alternative: Anthropic's built-in bash tool needs no schema at all —
    `{"type": "bash_20250124", "name": "bash"}` — Claude sends
    `{"command": "..."}` and you run it. Custom schemas (below) are used here
    so the demo can show how tool descriptions shape agent behaviour.
    """
    return [
        {
            "name": "find_files",
            "description": (
                "Find files in the working directory whose name matches a glob "
                "pattern. Returns a list of relative paths. Use this first to "
                "discover what files exist before reading them."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern for the file name, e.g. '*.py', '*.md', 'README*'",
                    },
                    "path": {
                        "type": "string",
                        "description": "Subdirectory to search, relative to the working directory (default: '.')",
                        "default": ".",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of paths to return (default: 50)",
                        "default": 50,
                    },
                },
                "required": ["pattern"],
            },
        },
        {
            "name": "read_file",
            "description": (
                "Read the contents of a file in the working directory. "
                "Returns the text with line numbers. For large files, pass "
                "start_line/end_line to read only the part you need — the "
                "whole file goes into context otherwise."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path relative to the working directory, e.g. 'src/agent.py'",
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "First line to read, 1-indexed (default: 1)",
                        "default": 1,
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "Last line to read, inclusive (default: end of file)",
                    },
                },
                "required": ["path"],
            },
        },
        {
            "name": "grep_files",
            "description": (
                "Search file contents in the working directory for a regular "
                "expression. Returns matching lines as 'path:line:text'. Use "
                "this to locate where something is defined or mentioned before "
                "reading the full file."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Regular expression to search for (grep -E syntax)",
                    },
                    "path": {
                        "type": "string",
                        "description": "File or subdirectory to search, relative to the working directory (default: '.')",
                        "default": ".",
                    },
                    "glob": {
                        "type": "string",
                        "description": "Only search files matching this glob, e.g. '*.py' (default: all files)",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of matching lines to return (default: 50)",
                        "default": 50,
                    },
                },
                "required": ["pattern"],
            },
        },
        {
            "name": "write_file",
            "description": (
                "Create or overwrite a file in the working directory with the given "
                "content. Use this whenever the user asks to write, save, or create "
                "a file. Content may be empty. Parent directories are created."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File path relative to the working directory, e.g. 'notes/lucas.md'",
                    },
                    "content": {
                        "type": "string",
                        "description": "Full text content of the file (default: empty)",
                        "default": "",
                    },
                },
                "required": ["file_path"],
            },
        }
    ]
    
def _safe_path(rel: str) -> Path:
    """Resolve a model-supplied path and refuse anything outside WORKDIR."""
    p = (WORKDIR / rel).resolve()
    if not p.is_relative_to(WORKDIR):
        raise ValueError(f"path escapes working directory: {rel}")
    return p


def _run(cmd: list[str]) -> str:
    """Run a command (no shell) and return stdout + stderr."""
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=WORKDIR)
    return (r.stdout + r.stderr).strip()


def execute_tool(name: str, tool_input: dict[str, Any]) -> str:
    """Run one tool by name. Returns a string to hand back as the tool_result."""
    try:
        if name == "find_files":
            root = _safe_path(tool_input.get("path", "."))
            out = _run(["find", str(root), "-type", "f", "-name", tool_input["pattern"]])
            lines = [str(Path(l).relative_to(WORKDIR)) for l in out.splitlines() if l]
            lines = lines[: tool_input.get("max_results", 50)]
            return "\n".join(lines) or "No files found."

        if name == "read_file":
            p = _safe_path(tool_input["path"])
            start = tool_input.get("start_line", 1)
            end = tool_input.get("end_line", "$")
            out = _run(["sed", "-n", f"{start},{end}p", str(p)])
            numbered = [f"{i}\t{l}" for i, l in enumerate(out.splitlines(), start=start)]
            return "\n".join(numbered) or "(empty)"

        if name == "grep_files":
            root = _safe_path(tool_input.get("path", "."))
            cmd = ["grep", "-rnE", "-m", str(tool_input.get("max_results", 50))]
            if glob := tool_input.get("glob"):
                cmd += ["--include", glob]
            cmd += [tool_input["pattern"], str(root)]
            out = _run(cmd)
            lines = out.replace(str(WORKDIR) + "/", "").splitlines()
            return "\n".join(lines[: tool_input.get("max_results", 50)]) or "No matches."
        if name == "write_file":
            p = _safe_path(tool_input["file_path"])
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(tool_input.get("content", ""))
            return f"Wrote {len(tool_input.get('content', ''))} chars to {p.relative_to(WORKDIR)}"
            

        return f"Unknown tool: {name}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    tools = get_tool_definitions()
    assert [t["name"] for t in tools] == ["find_files", "read_file", "grep_files", "write_file"]
    for t in tools:
        assert set(t) == {"name", "description", "input_schema"}
        assert t["input_schema"]["type"] == "object"
        for r in t["input_schema"].get("required", []):
            assert r in t["input_schema"]["properties"]
    assert "tools.py" in execute_tool("find_files", {"pattern": "*.py"})
    assert execute_tool("read_file", {"path": "tools.py", "start_line": 1, "end_line": 1}).startswith("1\t")
    assert "def execute_tool" in execute_tool("grep_files", {"pattern": "def execute_tool", "glob": "*.py"})
    assert execute_tool("read_file", {"path": "../../../etc/passwd"}).startswith("Error")
    assert "Wrote" in execute_tool("write_file", {"file_path": "_t.md", "content": "hi"}) and Path("_t.md").read_text() == "hi"; Path("_t.md").unlink()
    assert execute_tool("write_file", {"file_path": "../_t.md"}).startswith("Error")
    print("ok")
