# /// script
# requires-python = ">=3.12"
# dependencies = ["anthropic", "python-dotenv"]
# ///
"""
Act 1: Same Prompt, Three Schemas, Three Outputs.

Run: uv run structured_outputs_demo.py

This script demonstrates how structured outputs work through tool_choice.
The SAME user prompt is sent 3 times — each time forcing a different tool
schema. The model produces valid JSON matching each schema every time.

Key teaching point: the SCHEMA is context that shapes output structure.
The prompt provides the content; the schema provides the shape.
"""

from __future__ import annotations

import json
import sys

from dotenv import load_dotenv

load_dotenv()

import anthropic

MODEL = "claude-sonnet-4-20250514"

# ─── TEACHING MOMENT ──────────────────────────────────────────────
# One prompt. Three schemas. Three completely different outputs.
# The schema acts as a "mold" — the model pours its knowledge
# into whatever shape you provide. This is the core insight of
# structured outputs: you're engineering the OUTPUT context.
# ──────────────────────────────────────────────────────────────────

USER_PROMPT = "Explain the concept of recursion in programming"

# ─── TEACHING MOMENT ──────────────────────────────────────────────
# Each tool definition is a JSON Schema that constrains the model's
# output. We use tool_choice to FORCE the model to call a specific
# tool — this guarantees the output matches our schema exactly.
#
# In practice, this is how Claude's Artifacts work: the model calls
# a create_artifact tool with structured JSON, and the frontend
# renders it. Same pattern, production scale.
# ──────────────────────────────────────────────────────────────────

TOOL_SCHEMAS = [
    {
        "name": "create_explanation",
        "description": "Create a structured explanation of a concept",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Topic title"},
                "summary": {
                    "type": "string",
                    "description": "One paragraph overview",
                },
                "key_points": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "3-5 key takeaways",
                },
                "analogy": {
                    "type": "string",
                    "description": "A real-world analogy to aid understanding",
                },
            },
            "required": ["title", "summary", "key_points", "analogy"],
        },
    },
    {
        "name": "create_flashcards",
        "description": "Create a deck of flashcards for studying",
        "input_schema": {
            "type": "object",
            "properties": {
                "deck_title": {"type": "string"},
                "cards": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "front": {
                                "type": "string",
                                "description": "Question or term",
                            },
                            "back": {
                                "type": "string",
                                "description": "Answer or definition",
                            },
                        },
                        "required": ["front", "back"],
                    },
                    "minItems": 4,
                    "maxItems": 6,
                },
            },
            "required": ["deck_title", "cards"],
        },
    },
    {
        "name": "create_checklist",
        "description": "Create a learning checklist with steps to master a topic",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "step": {"type": "string", "description": "What to do"},
                            "detail": {
                                "type": "string",
                                "description": "Why this step matters",
                            },
                        },
                        "required": ["step", "detail"],
                    },
                    "minItems": 4,
                    "maxItems": 8,
                },
            },
            "required": ["title", "items"],
        },
    },
]


def run_demo():
    """Run the same prompt through 3 different schemas and display results."""
    client = anthropic.Anthropic()

    # ─── TEACHING MOMENT ──────────────────────────────────────────
    # We track token usage across all 3 calls to show that:
    # 1. Input tokens are nearly identical (same prompt + similar tool defs)
    # 2. Output tokens vary based on schema complexity
    # 3. The total cost is predictable from the schema design
    # ──────────────────────────────────────────────────────────────
    total_input = 0
    total_output = 0

    print("=" * 60)
    print("  STRUCTURED OUTPUTS DEMO")
    print("  Same prompt → 3 schemas → 3 different outputs")
    print("=" * 60)
    print(f'\n  Prompt: "{USER_PROMPT}"\n')

    for i, tool in enumerate(TOOL_SCHEMAS, 1):
        print(f"{'─' * 60}")
        print(f"  Schema {i}/3: {tool['name']}")
        print(f"{'─' * 60}")

        # ─── TEACHING MOMENT ──────────────────────────────────────
        # tool_choice forces the model to call this specific tool.
        # Without it, the model might respond with plain text instead.
        # This is the "guaranteed structured output" pattern.
        # ──────────────────────────────────────────────────────────
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=[tool],
            tool_choice={"type": "tool", "name": tool["name"]},
            messages=[{"role": "user", "content": USER_PROMPT}],
        )

        # Extract the structured output from the tool_use block
        tool_block = next(b for b in response.content if b.type == "tool_use")
        result = tool_block.input

        # Display
        print(json.dumps(result, indent=2))

        # Token accounting
        input_tok = response.usage.input_tokens
        output_tok = response.usage.output_tokens
        total_input += input_tok
        total_output += output_tok

        print(f"\n  Tokens: {input_tok} in → {output_tok} out")

    # Summary
    print(f"\n{'=' * 60}")
    print("  TOKEN SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Total input tokens:  {total_input:,}")
    print(f"  Total output tokens: {total_output:,}")
    print(f"  Total tokens:        {total_input + total_output:,}")
    print()
    print("  Notice: same prompt, same input cost, different output shapes.")
    print("  The SCHEMA is the context that determines structure.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    # Quick sanity check
    if not anthropic.Anthropic().api_key:
        print("Error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    run_demo()
