"""
Artifact schema registry — the foundation of structured output routing.

This module defines all 8 artifact types, their JSON schemas, and the
registry that tracks which artifacts have been created in a session.
The registry feeds dynamic context back into the system prompt.
"""

from __future__ import annotations


# ─── TEACHING MOMENT ──────────────────────────────────────────────
# Each artifact type has three parts:
#   1. description — what the model reads to decide WHEN to use it
#   2. when_to_use — routing hints injected into the system prompt
#   3. schema — JSON Schema that constrains the model's output
#
# The description + when_to_use text is "writing context" — it shapes
# the model's tool selection behavior. The schema is "selecting context"
# — it restricts which JSON structures count as valid output.
# ──────────────────────────────────────────────────────────────────

ARTIFACT_REGISTRY: dict[str, dict] = {
    "selectable_options": {
        "description": "A set of clickable option cards the user can choose from",
        "when_to_use": "When the topic is broad and you want the user to pick a direction or subtopic",
        "schema": {
            "type": "object",
            "properties": {
                "artifact_type": {
                    "type": "string",
                    "enum": ["selectable_options"],
                },
                "title": {"type": "string", "description": "Heading for the options"},
                "options": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "label": {
                                "type": "string",
                                "description": "Short name for the option",
                            },
                            "description": {
                                "type": "string",
                                "description": "1-2 sentence explanation",
                            },
                            "icon": {
                                "type": "string",
                                "description": "Single emoji representing this option",
                            },
                        },
                        "required": ["label", "description", "icon"],
                    },
                    "minItems": 2,
                    "maxItems": 6,
                },
            },
            "required": ["artifact_type", "title", "options"],
        },
    },
    "flashcard_deck": {
        "description": "A deck of flashcards with front/back for studying concepts",
        "when_to_use": "When the user wants to learn or memorize key concepts, definitions, or facts",
        "schema": {
            "type": "object",
            "properties": {
                "artifact_type": {
                    "type": "string",
                    "enum": ["flashcard_deck"],
                },
                "title": {"type": "string", "description": "Deck title"},
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
                    "minItems": 3,
                    "maxItems": 10,
                },
            },
            "required": ["artifact_type", "title", "cards"],
        },
    },
    "checklist": {
        "description": "An interactive checklist with progress tracking",
        "when_to_use": "When presenting steps, prerequisites, or a list of items to work through",
        "schema": {
            "type": "object",
            "properties": {
                "artifact_type": {
                    "type": "string",
                    "enum": ["checklist"],
                },
                "title": {"type": "string", "description": "Checklist title"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "The checklist item",
                            },
                            "detail": {
                                "type": "string",
                                "description": "Optional extra detail shown on hover",
                            },
                        },
                        "required": ["text"],
                    },
                    "minItems": 2,
                    "maxItems": 12,
                },
            },
            "required": ["artifact_type", "title", "items"],
        },
    },
    "flowchart": {
        "description": "A visual flowchart showing a process or decision tree",
        "when_to_use": "When explaining a process, algorithm, or decision flow with branches",
        "schema": {
            "type": "object",
            "properties": {
                "artifact_type": {
                    "type": "string",
                    "enum": ["flowchart"],
                },
                "title": {"type": "string", "description": "Flowchart title"},
                "nodes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "label": {
                                "type": "string",
                                "description": "Text inside the node",
                            },
                            "type": {
                                "type": "string",
                                "enum": ["start", "action", "decision", "end"],
                                "description": "Node shape: start/end=oval, action=rounded rect, decision=diamond",
                            },
                        },
                        "required": ["id", "label", "type"],
                    },
                    "minItems": 2,
                },
                "edges": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "from": {"type": "string", "description": "Source node id"},
                            "to": {"type": "string", "description": "Target node id"},
                            "label": {
                                "type": "string",
                                "description": "Optional edge label (e.g., Yes/No)",
                            },
                        },
                        "required": ["from", "to"],
                    },
                },
            },
            "required": ["artifact_type", "title", "nodes", "edges"],
        },
    },
    "semantic_zoom": {
        "description": "Content at three detail levels: TL;DR, Summary, and Deep Dive",
        "when_to_use": "When explaining a concept that benefits from multiple levels of detail",
        "schema": {
            "type": "object",
            "properties": {
                "artifact_type": {
                    "type": "string",
                    "enum": ["semantic_zoom"],
                },
                "title": {"type": "string", "description": "Topic title"},
                "tldr": {
                    "type": "string",
                    "description": "1-2 sentence ultra-brief summary",
                },
                "summary": {
                    "type": "string",
                    "description": "1-2 paragraph overview with key points",
                },
                "deep_dive": {
                    "type": "string",
                    "description": "Detailed explanation with examples and nuances",
                },
            },
            "required": ["artifact_type", "title", "tldr", "summary", "deep_dive"],
        },
    },
    "inline_quiz": {
        "description": "An interactive quiz with multiple-choice questions and scoring",
        "when_to_use": "When the user wants to test their understanding or asks to be quizzed",
        "schema": {
            "type": "object",
            "properties": {
                "artifact_type": {
                    "type": "string",
                    "enum": ["inline_quiz"],
                },
                "title": {"type": "string", "description": "Quiz title"},
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "options": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 3,
                                "maxItems": 4,
                            },
                            "correct_index": {
                                "type": "integer",
                                "description": "0-based index of the correct option",
                            },
                            "explanation": {
                                "type": "string",
                                "description": "Why this answer is correct",
                            },
                        },
                        "required": [
                            "question",
                            "options",
                            "correct_index",
                            "explanation",
                        ],
                    },
                    "minItems": 3,
                    "maxItems": 8,
                },
            },
            "required": ["artifact_type", "title", "questions"],
        },
    },
    "timeline": {
        "description": "An interactive horizontal timeline showing events in chronological order",
        "when_to_use": "When the question involves chronological order, history, evolution of ideas, sequences of events, or any 'when did X happen' style query",
        "schema": {
            "type": "object",
            "properties": {
                "artifact_type": {
                    "type": "string",
                    "enum": ["timeline"],
                },
                "title": {"type": "string", "description": "Timeline title"},
                "events": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date or time label (e.g. '1969', 'March 2020', '500 BC')",
                            },
                            "title": {
                                "type": "string",
                                "description": "Short event title",
                            },
                            "description": {
                                "type": "string",
                                "description": "1-2 sentence description of what happened",
                            },
                        },
                        "required": ["date", "title", "description"],
                    },
                    "minItems": 3,
                    "maxItems": 12,
                },
            },
            "required": ["artifact_type", "title", "events"],
        },
    },
    "concept_explorer": {
        "description": "A visual concept map with labeled dots on a 2D scatter plot",
        "when_to_use": "When showing how multiple concepts relate along two dimensions, or giving a big-picture overview",
        "schema": {
            "type": "object",
            "properties": {
                "artifact_type": {
                    "type": "string",
                    "enum": ["concept_explorer"],
                },
                "title": {"type": "string", "description": "Explorer title"},
                "x_axis": {
                    "type": "string",
                    "description": "Label for horizontal axis",
                },
                "y_axis": {
                    "type": "string",
                    "description": "Label for vertical axis",
                },
                "concepts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Concept name"},
                            "x": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 100,
                                "description": "X position (0-100)",
                            },
                            "y": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 100,
                                "description": "Y position (0-100)",
                            },
                            "description": {
                                "type": "string",
                                "description": "Brief tooltip description",
                            },
                        },
                        "required": ["name", "x", "y", "description"],
                    },
                    "minItems": 3,
                    "maxItems": 10,
                },
            },
            "required": [
                "artifact_type",
                "title",
                "x_axis",
                "y_axis",
                "concepts",
            ],
        },
    },
}


def get_artifact_descriptions() -> str:
    """
    Format artifact type descriptions for injection into the system prompt.

    # ─── TEACHING MOMENT ──────────────────────────────────────────
    # This is "writing context" — we're telling the model what artifact
    # types exist and when to use each one. The model reads this text
    # on every API call, so it always knows its options.
    #
    # Cost: ~400 tokens of static overhead per request.
    # Benefit: the model reliably picks the right artifact type.
    # ──────────────────────────────────────────────────────────────
    """
    lines = ["Available artifact types:\n"]
    for name, info in ARTIFACT_REGISTRY.items():
        lines.append(f"- **{name}**: {info['description']}")
        lines.append(f"  Use when: {info['when_to_use']}")
    return "\n".join(lines)


def get_artifact_tool() -> dict:
    """
    Build a single Anthropic tool definition with a flat merged schema.

    # ─── TEACHING MOMENT ──────────────────────────────────────────
    # The Anthropic API does NOT allow anyOf/oneOf/allOf at the top
    # level of input_schema. So instead of a discriminated union, we
    # use a FLAT schema that merges all properties from all 7 types.
    #
    # The `artifact_type` enum field acts as the discriminator — the
    # model picks a type, then fills only the relevant fields. The
    # system prompt descriptions (from get_artifact_descriptions())
    # tell the model which fields belong to which type.
    #
    # This is actually the production pattern: one tool, one flat
    # schema, many types. Token-efficient + easy to extend.
    # ──────────────────────────────────────────────────────────────
    """
    # Merge all properties from all artifact schemas into one flat schema
    all_properties = {
        "artifact_type": {
            "type": "string",
            "enum": list(ARTIFACT_REGISTRY.keys()),
            "description": "The type of artifact to create",
        },
    }
    for info in ARTIFACT_REGISTRY.values():
        for prop_name, prop_schema in info["schema"]["properties"].items():
            if prop_name == "artifact_type":
                continue  # Already handled above with merged enum
            if prop_name not in all_properties:
                all_properties[prop_name] = prop_schema

    return {
        "name": "create_artifact",
        "description": (
            "Create an interactive artifact to display to the user. "
            "Choose the artifact_type based on the content and context. "
            "The artifact will be rendered as an interactive element. "
            "Only include the fields relevant to the chosen artifact_type."
        ),
        "input_schema": {
            "type": "object",
            "properties": all_properties,
            "required": ["artifact_type", "title"],
        },
    }


class ArtifactRegistry:
    """
    Track created artifacts within a session for dynamic context injection.

    # ─── TEACHING MOMENT ──────────────────────────────────────────
    # This is the "dynamic context layer." As the user interacts,
    # the registry builds a summary of what artifacts exist. This
    # summary gets injected into the system prompt so the model knows
    # what it has already created — enabling coherent follow-ups.
    #
    # Without this, the model might recreate the same flashcards
    # or lose track of what topics have been explored.
    # ──────────────────────────────────────────────────────────────
    """

    def __init__(self):
        self.artifacts: list[dict] = []

    def register(self, artifact: dict) -> int:
        """Store an artifact and return its index."""
        self.artifacts.append(artifact)
        return len(self.artifacts) - 1

    def get_context_summary(self) -> str:
        """
        Generate a summary string for system prompt injection.

        Returns empty string if no artifacts yet (saves tokens on turn 1).
        """
        if not self.artifacts:
            return ""

        lines = [f"\nArtifacts created so far ({len(self.artifacts)} total):"]
        for i, artifact in enumerate(self.artifacts):
            a_type = artifact.get("artifact_type", "unknown")
            title = artifact.get("title", "Untitled")
            lines.append(f"  {i + 1}. [{a_type}] {title}")
        lines.append(
            "\nBuild on these artifacts when relevant. "
            "Reference previous content rather than repeating it."
        )
        return "\n".join(lines)
