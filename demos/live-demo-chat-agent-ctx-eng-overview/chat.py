#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "anthropic>=0.115.0",
#   "prompt-toolkit==3.0.52",
# ]
# ///
import os
import anthropic
# import prompt_toolkit

MAX_ROUNDS = 10
MODEL_NAME = "claude-sonnet-4-6"
SYSTEM_PROMPT = "You are a helpful assistant that can search the web, create and read files."


def create_file(filepath: str, content: str):
    """Creates a file"""
    with open(filepath, "w+") as f:
        f.write(content)
    
    return "File has been created"

def read_file(filepath: str):
    """Read a file"""
    with open(filepath, "r") as f:
        contents = f.read()
    
    return contents
    

def search_files(folder_path: str):
    """Recursively list all files inside a folder and its nested directories."""
    if not os.path.isdir(folder_path):
        return f"Error: '{folder_path}' is not a directory."

    matches = []
    for root, _dirs, files in os.walk(folder_path):
        # skip hidden/noise directories to keep results useful
        _dirs[:] = [d for d in _dirs if d not in {".git", "__pycache__", ".venv", "node_modules"}]
        for name in files:
            matches.append(os.path.join(root, name))

    if not matches:
        return f"No files found under '{folder_path}'."
    return "\n".join(sorted(matches))


def get_tool_definitions():
    """Definitions for the tools the agent will use."""
    tool_defs = [
        {"type": "web_search_20260209", "name": "web_search"},
        {
            "name": "read_file",
            "description": "Function that reads a .txt or .md file.",
            "input_schema": {
                "type": "object",
                "properties": {
                "filepath": {
                    "type": "string",
                    "description": "The path to the file to read"
                },
                },
                "required": ["filepath"]
            }
            },
        {
            "name": "create_file",
            "description": "Function that creates a .txt or .md file.",
            "input_schema": {
                "type": "object",
                "properties": {
                "filepath": {
                    "type": "string",
                    "description": "The path to the file to read"
                },
                "content": {
                    "type": "string",
                    "description": "The contents to write to a file."
                },
                
                },
                "required": ["filepath"]
            }
            },
        {
            "name": "search_files",
            "description": "Function searches a directory for all files inside and inside nested directories.",
            "input_schema": {
                "type": "object",
                "properties": {
                "folder_path": {
                    "type": "string",
                    "description": "The path to the folder where to search for files."
                },
                },
                "required": ["folder_path"]
            }
            }

    ]
    return tool_defs

TOOL_FUNCTIONS = {
    "web_search": "",
    "read_file": read_file,
    "create_file": create_file,
    "search_files": search_files,
}


def execute_tool(name: str, tool_input: dict) -> str:
    """Dispatch a tool_use block to its Python function and return a string result."""
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return f"Error: unknown tool '{name}'."
    try:
        return str(func(**tool_input))
    except Exception as e:
        return f"Error running tool '{name}': {e}"

class Agent:
    # Implement the logic of the agent and conversation history
    """An agent with explicit context window management."""
    
    def __init__(self, ):
        
        # Send messages to the anthropic API and get responses back
        self.client = anthropic.Anthropic()
        self.messages: list[dict] = [] # The context window
        #self.stats = Stats for the Context Window at any given moment
        self.tool_definitions = get_tool_definitions()
    
    def _call_api(self):
        """
        Make a single API call with the current context.
        """
        response = self.client.messages.create(
            model=MODEL_NAME,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=self.tool_definitions,
            messages=self.messages,
        )
        
        return response
    
    
    def run_turn(self, user_input: str) -> str:
        """
        Run one full turn: user input → (possible tool calls) → final response.

        Returns the assistant's final text response.
        """
        
        self.messages.append({"role": "user", "content": user_input})
        
        final_text = ""
        for round_num in range(MAX_ROUNDS):
            response = self._call_api()
            tool_use_blocks = [
                block for block in response.content if block.type=="tool_use"
            ]
            
            if response.stop_reason == "tool_use" and tool_use_blocks:
                self.messages.append({"role": "assistant",
                                      "content": response.content})
                
                # Execute each tool and collect results
                tool_results = []
                for block in tool_use_blocks:
                    # display.tool_call(block.name, block.input)

                    result_text = execute_tool(block.name, block.input)
                    # display.tool_result(block.name, result_text)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result_text,
                        }
                    )

                self.messages.append({"role": "user", "content": tool_results})
            else:
                # FInal response extract text and append to context
                text_blocks = [
                    block.text for block in response.content
                    if hasattr(block, "text")
                ]
                final_text = "\n".join(text_blocks)
                self.messages.append(
                    {"role": "assistant", "content": response.content}
                )
                break
        
        else:
            final_text = "Reached maximum tool rounds"
        
        
        return final_text

    def clear_context(self) -> None:
        """Reset the conversation - clear messages from the context window"""
        self.messages.clear()


def chat_session():
    agent = Agent()
    while True:
        msg = input("User msg: ")
        if msg == "quit" or msg == "q":
            # this interrupts the conversation
            break
        elif msg == "clear":
            agent.clear_context()
            print("Context cleared.")
            continue
        elif msg == "help":
            print("Commands available: ")
            for tool in TOOL_FUNCTIONS.keys():
                print(tool)
        response = agent.run_turn(msg)
        print(f"Assistant: {response}")


if __name__ == "__main__":
    chat_session()
        

