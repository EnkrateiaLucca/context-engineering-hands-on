"""
Hand-rolled agent loop with explicit context management.

This is the CORE teaching module. Every context engineering decision
is visible — no framework magic hides how the messages array grows,
how tool results enter context, or how tokens accumulate.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import anthropic

import display
from retrieval import KnowledgeBase
from tools import execute_tool, get_tool_definitions


# ─── TEACHING MOMENT ──────────────────────────────────────────────
# The system prompt is "writing context" — the first lever.
# It shapes every response the agent produces. Notice how we:
# 1. Define the agent's role and capabilities
# 2. Set behavioral constraints (cite sources, be concise)
# 3. Tell it about its tools (the model reads this + tool schemas)
#
# This prompt consumes ~200 tokens on EVERY API call — it's a
# fixed cost that you pay for the entire conversation.
# ──────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are a knowledgeable assistant with access to a document knowledge base \
about context engineering for LLMs and agentic systems.

Your behavior:
- Use your tools to search for and retrieve relevant documents before answering
- Always cite which document(s) informed your answer (use document IDs)
- Be concise but thorough — aim for 2-3 paragraph responses
- If a question is outside the knowledge base, say so honestly

Available tools:
- search_documents: Find relevant documents by keyword query
- get_document: Retrieve full content of a specific document by ID
- list_documents: See all available documents and their metadata
"""

MODEL = "claude-sonnet-4-6"
MAX_TOOL_ROUNDS = 10  # Safety limit to prevent infinite tool loops


@dataclass
class ContextStats:
    """Track token usage and interaction counts across the session."""

    turn_count: int = 0
    tool_call_count: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0

    # Per-turn tracking (reset each turn)
    turn_input_tokens: int = 0
    turn_output_tokens: int = 0

    def record_usage(self, usage) -> None:
        """Record token usage from an API response."""
        input_tok = getattr(usage, "input_tokens", 0)
        output_tok = getattr(usage, "output_tokens", 0)
        self.turn_input_tokens += input_tok
        self.turn_output_tokens += output_tok
        self.total_input_tokens += input_tok
        self.total_output_tokens += output_tok

    def new_turn(self) -> None:
        """Start tracking a new turn."""
        self.turn_count += 1
        self.turn_input_tokens = 0
        self.turn_output_tokens = 0


class Agent:
    """
    An agent with explicit context window management.

    # ─── TEACHING MOMENT ──────────────────────────────────────────
    # self.messages IS the context window. Every element in this list
    # gets sent to the API on every call. Understanding this list is
    # understanding context engineering:
    # - User messages: what the human asked
    # - Assistant messages: what the model responded (including tool calls)
    # - Tool results: what tools returned (injected as user-role messages)
    #
    # After 5 turns with tool use, this list might have 20+ entries
    # and consume 10,000+ tokens — all re-processed on each API call.
    # ──────────────────────────────────────────────────────────────
    """

    def __init__(self, kb: KnowledgeBase):
        self.client = anthropic.Anthropic()
        self.kb = kb
        self.messages: list[dict] = []  # THE context window
        self.stats = ContextStats()
        self.tool_definitions = get_tool_definitions()

    def run_turn(self, user_input: str) -> str:
        """
        Run one full turn: user input → (possible tool calls) → final response.

        Returns the assistant's final text response.
        """
        self.stats.new_turn()

        # ─── TEACHING MOMENT ──────────────────────────────────────
        # Step 1: Append user message to context.
        # This is straightforward, but notice that in a long session,
        # ALL previous user messages are still here. The context grows
        # monotonically — nothing is removed unless we explicitly clear it.
        # ──────────────────────────────────────────────────────────
        self.messages.append({"role": "user", "content": user_input})

        # ─── TEACHING MOMENT ──────────────────────────────────────
        # The agent loop: we keep calling the API until the model
        # produces a final text response (stop_reason != "tool_use").
        # Each iteration may add 2+ messages to context:
        #   - The assistant's response (with tool_use blocks)
        #   - The tool_result message(s)
        # This is how context grows FAST in agentic systems.
        # ──────────────────────────────────────────────────────────
        final_text = ""
        for round_num in range(MAX_TOOL_ROUNDS):
            response = self._call_api()
            # Check if the model wants to use tools
            tool_use_blocks = [
                block for block in response.content if block.type == "tool_use"
            ]

            if response.stop_reason == "tool_use" and tool_use_blocks:
                # ─── TEACHING MOMENT ──────────────────────────────
                # The assistant's response (including tool_use blocks)
                # is appended to messages as-is. The model's "thinking"
                # about which tools to call is now part of the context.
                # ──────────────────────────────────────────────────
                self.messages.append(
                    {"role": "assistant", "content": response.content}
                )

                # Execute each tool and collect results
                tool_results = []
                for block in tool_use_blocks:
                    self.stats.tool_call_count += 1
                    display.tool_call(block.name, block.input)

                    result_text = execute_tool(block.name, block.input, self.kb)
                    display.tool_result(block.name, result_text)

                    # ─── TEACHING MOMENT ──────────────────────────
                    # Tool results enter context as user-role messages
                    # with type "tool_result". This is how retrieved
                    # documents get INTO the context window — the
                    # "selecting context" lever in action.
                    #
                    # A full document might be 500+ tokens. Every
                    # get_document call adds that many tokens to the
                    # window PERMANENTLY (until /clear).
                    # ──────────────────────────────────────────────
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result_text,
                        }
                    )

                self.messages.append({"role": "user", "content": tool_results})
            else:
                # Final response — extract text and append to context
                text_blocks = [
                    block.text
                    for block in response.content
                    if hasattr(block, "text")
                ]
                final_text = "\n".join(text_blocks)
                self.messages.append(
                    {"role": "assistant", "content": response.content}
                )
                break
        else:
            final_text = "(Reached maximum tool rounds — something may be wrong)"

        # ─── TEACHING MOMENT ──────────────────────────────────────
        # After each turn, we display context stats so students can
        # see the REAL cost of this conversation. Input tokens grow
        # every turn because the ENTIRE messages array is re-sent.
        # ──────────────────────────────────────────────────────────
        display.context_stats(
            turn_count=self.stats.turn_count,
            message_count=len(self.messages),
            tool_call_count=self.stats.tool_call_count,
            input_tokens=self.stats.total_input_tokens,
            output_tokens=self.stats.total_output_tokens,
        )

        return final_text

    def _call_api(self):
        """
        Make a single API call with the current context.

        # ─── TEACHING MOMENT ──────────────────────────────────────
        # This is where context meets the API. Notice what gets sent:
        # - model: which model (affects context window size)
        # - system: the system prompt (~200 tokens, every call)
        # - tools: tool definitions (~800 tokens, every call)
        # - messages: the FULL conversation history (grows each turn)
        #
        # The input token count = system + tools + all messages.
        # response.usage tells us the exact cost.
        # ──────────────────────────────────────────────────────────
        """
        response = self.client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=self.tool_definitions,
            messages=self.messages,
        )
        self.stats.record_usage(response.usage)
        return response

    def get_context_snapshot(self) -> list[dict]:
        """Return the raw messages array for inspection."""
        return self.messages

    def get_stats(self) -> ContextStats:
        """Return cumulative session statistics."""
        return self.stats

    def clear_context(self) -> None:
        """
        Reset the conversation — clear messages and stats.

        In a production agent, you might instead compress old messages
        into a summary rather than deleting them entirely.
        """
        self.messages.clear()
        self.stats = ContextStats()
