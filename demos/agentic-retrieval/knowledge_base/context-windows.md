---
id: context-windows
title: "Understanding Context Windows in LLMs"
tags: [context-window, tokens, fundamentals]
---

# Understanding Context Windows in LLMs

The context window is the fixed-size buffer of tokens that a language model can attend to during a single inference call. Every token in the window — system prompt, conversation history, tool definitions, retrieved documents, and the model's own response — competes for the same limited space.

## How Context Windows Work

Modern LLMs process text as sequences of tokens (roughly half to ¾ of a word each, depending on the tokenizer). The context window defines the maximum number of tokens the model can read and generate in one pass. Once tokens exceed the window, earlier tokens are either truncated or the request fails entirely.

Key specifications as of October 2026:
- **Claude Fable 5.1 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5**: 1M tokens
- **GPT-6 Astra**: 1.05M tokens
- **Gemini 4 Argon**: 1M tokens

## Why Size Alone Doesn't Matter

A larger context window does not automatically mean better performance. Research consistently shows that models struggle with information in the "middle" of long contexts — a phenomenon called the **Lost in the Middle** effect. Placing critical instructions at the very beginning or very end of the context yields significantly better recall.

## The Token Budget Analogy

Think of context as a financial budget. Every element has a cost:

| Element | Typical Cost |
|---------|-------------|
| System prompt | 200–2,000 tokens |
| Tool definitions (5 tools) | 1,500–3,000 tokens |
| Retrieved documents | 500–5,000 tokens each |
| Conversation history (10 turns) | 2,000–10,000 tokens |

Without careful management, these costs compound across turns in an agentic loop, consuming the entire budget before the model can produce useful output.

## Implications for Context Engineering

Context engineering treats the window as a **scarce resource** to be deliberately managed, not passively filled. The four key operations — write, select, compress, and isolate — each address a different aspect of window management.
