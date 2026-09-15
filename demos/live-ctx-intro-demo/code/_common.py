"""Shared helpers for the intro demos. Not a framework, just three functions."""
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
MODEL = "claude-sonnet-5"
client = anthropic.Anthropic()
ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")


def count(messages, system=None, tools=None) -> int:
    """Tokens the model will actually see for this call."""
    kw = {"model": MODEL, "messages": messages}
    if system:
        kw["system"] = system
    if tools:
        kw["tools"] = tools
    return client.messages.count_tokens(**kw).input_tokens


def ask(messages, system=None, tools=None, max_tokens=300):
    kw = {"model": MODEL, "messages": messages, "max_tokens": max_tokens}
    if system:
        kw["system"] = system
    if tools:
        kw["tools"] = tools
    return client.messages.create(**kw)


def text(resp) -> str:
    return "".join(b.text for b in resp.content if b.type == "text")
