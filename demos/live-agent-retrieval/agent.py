# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "anthropic>=1.6.0",
# ]
# ///
"""
Simple agent with access to some tools +
ability to answer questions from documents.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import anthropic

from tools import get_tool_definitions, execute_tool

SYSTEM_PROMPT = """
You are an agent that uses tools to solve tasks and answer questions
for the user.
"""

MODEL = "claude-sonnet-5"
MAX_TOOL_ROUNDS = 10


class Agent:
    """
    Agent = LLM + tools in a loop! Let's build that into this class!
    """
    def __init__(self):
        # you must have your anthropic api key as an env variable
        # if you don't! run: load_env from dot_env library
        self.client = anthropic.Anthropic()
        # messages exchanged, tools used, tool results
        self.messages: list[dict] = []
        # tool definitions
        self.tool_definitions = get_tool_definitions()
    
    def run_turn(self, user_input: str) -> str:
        """
        Run one full turn: user input → (possible tool calls) → final response.

        Returns the assistant's final text response.
        """
        
        self.messages.append({"role": "user", "content": user_input})
        final_text = ""
        for round_num in range(MAX_TOOL_ROUNDS):
            response = self._call_api()
            # Check if the model wants to use tools
            tool_use_blocks = [
                block for block in response.content if block.type == "tool_use"
            ]
            if response.stop_reason == "tool_use" and tool_use_blocks:
                self.messages.append(
                    {"role": "assistant", "content": response.content}
                )
            # Execute each tool and collect results
                tool_results = []
                for block in tool_use_blocks:
                    print(block.name, block.input)
                    result_text = execute_tool(block.name, block.input)
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
        
        return final_text
        
        
    def _call_api(self):
        """
        Calls the LLM Api (in this case Anthropic)
        ─────────────────────────────────────────────────────────
        """
        response = self.client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=self.tool_definitions,
            messages=self.messages,
        )

        return response

agent = Agent()
print(agent.run_turn("summarize the python files in this folder in 3 bullets"))
                
                    
                    
                    
                
                
            
            
        
        
        
        
        
    
    



