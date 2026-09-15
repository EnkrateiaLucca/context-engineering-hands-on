# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic"]
# ///

import csv
import random
import subprocess
import sys
from pathlib import Path

import anthropic

MODEL = "claude-opus-5"
DATA_DIR = Path(__file__).parent / "data"
OUT_DIR = Path(__file__).parent / "output"
SKILLS = [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
TOOLS = [{"type": "code_execution_20250825", "name": "code_execution"}]

def build_deck(client: anthropic.Anthropic, inputs: list[Path]) -> anthropic.types.Message:
    uploads = [client.files.upload(file=p) for p in inputs]
    for p, u in zip(inputs, uploads):
        print(f"uploaded {p.name} -> {u.id}")
    
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": (
                "You have a sales CSV and a notes.md with instructions from the presenter. "
                "Analyze the CSV with Python, then build a .pptx that follows notes.md exactly. "
                "Include at least one chart image generated from the data. "
                "Save the deck as sales_readout.pptx in the working directory."
            )},
            *[{"type": "container_upload", "file_id": u.id} for u in uploads],
        ],
    }]
    
    container = {"skills": SKILLS}
    while True:
        with client.messages.stream(
            model=MODEL,
            max_tokens=16000,
            container=container,
            messages=messages,
            tools=TOOLS,
        ) as stream:
            response = stream.get_final_message()
        print(f"stop_reason={response.stop_reason}")
        if response.stop_reason != "pause_turn":  # long sandbox runs pause; resume with same container
            return response
        messages.append({"role": "assistant", "content": response.content})
        container = {"id": response.container.id, "skills": SKILLS}
        
def download_outputs(client: anthropic.Anthropic, response: anthropic.types.Message) -> list[Path]:
    OUT_DIR.mkdir(exist_ok=True)
    saved = []
    for block in response.content:
        if block.type != "bash_code_execution_tool_result":
            continue
        result = block.content
        if result.type != "bash_code_execution_result":
            continue
        for f in result.content:
            meta = client.files.retrieve_metadata(file_id=f.file_id)
            dest = OUT_DIR / meta.filename
            client.files.download(file_id=f.file_id).write_to_file(dest)
            saved.append(dest)
            print(f"downloaded {dest}")
    return saved
    
def main() -> None:
    inputs = (sorted(DATA_DIR.glob("*")))
    client = anthropic.Anthropic()
    response = build_deck(client, inputs)

    if response.stop_reason == "refusal":
        sys.exit(f"refused: {response.stop_details}")

    for block in response.content:
        if block.type == "text":
            print(block.text)

    saved = download_outputs(client, response)
    decks = [p for p in saved if p.suffix == ".pptx"]
    if not decks:
        sys.exit("no .pptx came back; see text above")
    if sys.platform == "darwin":
        subprocess.run(["open", decks[0]])

if __name__ == "__main__":
    main()