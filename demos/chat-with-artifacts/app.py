# /// script
# requires-python = ">=3.12"
# dependencies = ["anthropic", "fastapi", "uvicorn", "python-dotenv"]
# ///
"""
Chat with Artifacts — FastAPI backend.

Run: uv run app.py
Then open: http://127.0.0.1:8000

This backend demonstrates context engineering in a chat application:
- 3-layer system prompt (persona + artifact types + session state)
- Tool-use for structured output (single create_artifact tool)
- Conversation history as growing context window
- Dynamic context injection from artifact registry
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()

import anthropic
import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from schemas import ArtifactRegistry, get_artifact_descriptions, get_artifact_tool

MODEL = "claude-sonnet-4-6"

# ─── TEACHING MOMENT ──────────────────────────────────────────────
# The system prompt is built from 3 layers, each with a different
# lifecycle and token cost:
#
# Layer 1: BASE_PERSONA — fixed text, ~150 tokens, never changes
# Layer 2: ARTIFACT_DESCRIPTIONS — static per session, ~400 tokens
# Layer 3: Dynamic state — grows as artifacts are created, 0-200 tokens
#
# Total system prompt: ~550 tokens (turn 1) → ~750 tokens (turn 10)
# This is the "writing context" lever — we're programming the model's
# behavior and knowledge on every API call.
# ──────────────────────────────────────────────────────────────────

BASE_PERSONA = """\
You are a helpful learning assistant that creates interactive artifacts \
to help users explore topics. You are conversational, encouraging, and \
focused on making learning engaging.

Rules:
- If the user would benefit from an artifact, create ONE artifact per response
- Keep your text response brief (1-3 sentences) to introduce the artifact
- When a user clicks an option or asks a follow-up, build on previous context
- Match the artifact type to the user's intent and conversation stage:
  - New topic → selectable_options (let them choose a direction)
  - Wants to learn → semantic_zoom or flashcard_deck
  - Wants to practice → inline_quiz
  - Wants process/flow → flowchart
  - Wants big picture → concept_explorer
  - Wants a task list → checklist
- If the user asks to be quizzed, reference content from earlier in the conversation
"""

ARTIFACT_DESCRIPTIONS = get_artifact_descriptions()
ARTIFACT_TOOL = get_artifact_tool()


@dataclass
class ConversationState:
    """
    Holds the full state for one chat session.

    # ─── TEACHING MOMENT ──────────────────────────────────────────
    # messages IS the context window. Every element gets sent to the
    # API on every call. After 10 turns with artifacts, this might
    # contain 30+ messages and 5,000+ tokens — all re-processed
    # each time. The stats track this growth so students can see it.
    # ──────────────────────────────────────────────────────────────
    """

    messages: list[dict] = field(default_factory=list)
    artifact_registry: ArtifactRegistry = field(default_factory=ArtifactRegistry)
    turn_count: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0


# ─── TEACHING MOMENT ──────────────────────────────────────────────
# In-memory state, keyed by session ID. In production you'd use
# Redis or a database, but for a teaching demo this makes the
# state management completely transparent.
# ──────────────────────────────────────────────────────────────────
sessions: dict[str, ConversationState] = {}


def build_system_prompt(state: ConversationState) -> str:
    """
    Construct the 3-layer system prompt.

    # ─── TEACHING MOMENT ──────────────────────────────────────────
    # This function assembles the system prompt from three layers:
    #
    # 1. BASE_PERSONA — who the model is and how it behaves (fixed)
    # 2. ARTIFACT_DESCRIPTIONS — what tools are available (static)
    # 3. Dynamic state — what has happened so far (grows)
    #
    # The dynamic layer is the key insight: as the user interacts,
    # the system prompt EVOLVES to include context about what
    # artifacts already exist. This is the "writing context" lever.
    # ──────────────────────────────────────────────────────────────
    """
    layers = [BASE_PERSONA, ARTIFACT_DESCRIPTIONS]

    # Layer 3: Dynamic session state (only if artifacts exist)
    artifact_summary = state.artifact_registry.get_context_summary()
    if artifact_summary:
        layers.append(artifact_summary)

    return "\n\n".join(layers)


app = FastAPI(title="Chat with Artifacts")
client = anthropic.Anthropic()


@app.post("/api/chat")
async def chat(request: Request) -> JSONResponse:
    """
    Main chat endpoint: user message → Claude → text + artifact.

    Flow:
    1. Get or create session state
    2. Append user message to conversation history
    3. Build 3-layer system prompt
    4. Call Claude with create_artifact tool
    5. Extract text response + any artifact
    6. Register artifact in session state
    7. Return response with context stats
    """
    body = await request.json()
    user_message = body.get("message", "")
    session_id = body.get("session_id", "default")

    # Get or create session
    if session_id not in sessions:
        sessions[session_id] = ConversationState()
    state = sessions[session_id]

    state.turn_count += 1
    state.messages.append({"role": "user", "content": user_message})

    # Build the layered system prompt
    system_prompt = build_system_prompt(state)

    # ─── TEACHING MOMENT ──────────────────────────────────────────
    # This is where everything comes together:
    # - system: our 3-layer prompt (~550-750 tokens)
    # - tools: single create_artifact tool (~200 tokens)
    # - messages: full conversation history (grows each turn)
    #
    # The model sees ALL of this on every call. Students can
    # watch the input token count climb in the stats bar.
    # ──────────────────────────────────────────────────────────────
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system_prompt,
        tools=[ARTIFACT_TOOL],
        messages=state.messages,
    )

    # Track token usage
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    state.total_input_tokens += input_tokens
    state.total_output_tokens += output_tokens

    # Extract text and artifact from response
    text_parts = []
    artifact = None

    for block in response.content:
        if hasattr(block, "text"):
            text_parts.append(block.text)
        elif block.type == "tool_use" and block.name == "create_artifact":
            artifact = block.input
            state.artifact_registry.register(artifact)

    assistant_text = " ".join(text_parts)

    # ─── TEACHING MOMENT ──────────────────────────────────────────
    # We store the model's FULL response (including tool_use blocks)
    # in the conversation history. This is critical: the model needs
    # to see its own tool calls to maintain coherent conversation.
    #
    # If we stripped out tool_use blocks, the model would "forget"
    # what artifacts it created — breaking the context chain.
    # ──────────────────────────────────────────────────────────────
    state.messages.append({"role": "assistant", "content": response.content})

    # If the model used a tool, we need to add the tool result
    # so the conversation stays valid for the API
    if artifact is not None:
        tool_use_block = next(
            b for b in response.content if b.type == "tool_use"
        )
        state.messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": "Artifact displayed to user successfully.",
                    }
                ],
            }
        )

    return JSONResponse(
        {
            "text": assistant_text,
            "artifact": artifact,
            "stats": {
                "turn_count": state.turn_count,
                "message_count": len(state.messages),
                "artifact_count": len(state.artifact_registry.artifacts),
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_input_tokens": state.total_input_tokens,
                "total_output_tokens": state.total_output_tokens,
                "system_prompt_preview": system_prompt[:200] + "...",
            },
        }
    )


@app.post("/api/reset")
async def reset(request: Request) -> JSONResponse:
    """Clear session state — fresh conversation."""
    body = await request.json()
    session_id = body.get("session_id", "default")
    sessions.pop(session_id, None)
    return JSONResponse({"status": "ok"})


@app.get("/")
async def index():
    """Serve the single-file frontend."""
    return FileResponse("static/index.html")


# Mount static files for any additional assets
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        print("  export ANTHROPIC_API_KEY=sk-ant-...", file=sys.stderr)
        sys.exit(1)

    print("Starting Chat with Artifacts...")
    print("  Open: http://127.0.0.1:8000")
    print("  Press Ctrl+C to stop\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
