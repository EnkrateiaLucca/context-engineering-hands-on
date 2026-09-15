# /// script
# dependencies = [
#   "anthropic",
# ]
# ///
# Can you read this?

import os
import sys
import json
from anthropic import Anthropic
 
MODEL = "claude-sonnet-5"

TOOLS = [
    {
        "name": "calculator",
        "description": "Evaluate a basic arithmetic expression, e.g. '17 * 23'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The arithmetic expression to evaluate.",
                }
            },
            "required": ["expression"],
        },
    },
]


def calculator(expression: str) -> str:
    """Evaluate a simple math expression"""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "Error: only basic arithmetic characters are allowed."
    return str(eval(expression))  

TOOL_FUNCTIONS = {"calculator": calculator}   



client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
def run_agent(user_input: str, max_turns: int = 10) -> str:
    messages = [{"role": "user", "content": user_input}]
 
    for _ in range(max_turns):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )
 
        # Whatever the model said (text and/or tool requests) goes back into history.
        messages.append({"role": "assistant", "content": response.content})
 
        # No tool requested -> the model is done talking. Exit the loop.
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")
 
        # Otherwise: run every tool it asked for, and hand back the results.
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            print(f"  [tool] {block.name}({json.dumps(block.input)})")
            output = TOOL_FUNCTIONS[block.name](**block.input)
            print(f"  [result] {output[:200]}")
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                }
            )
 
        messages.append({"role": "user", "content": results})
 
    return "Stopped: hit the maximum number of turns."

if __name__=="__main__":
    question = "How much is 10 + 10 * 30?"
    print(run_agent(question))
    
 

