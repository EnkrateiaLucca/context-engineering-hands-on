# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic"]
# ///
"""
Agent + Skill demo: Claude turns a CSV and a notes file into a .pptx deck.

Skills = context that is loaded only when needed. Instead of stuffing
python-pptx instructions into the prompt, we attach Anthropic's managed `pptx`
skill to the code-execution container. Claude reads the SKILL.md on demand,
writes the deck in the sandbox, and hands back a file_id we download.

    uv run pptx_from_data_agent.py            # generates data, builds deck
    uv run pptx_from_data_agent.py --no-gen   # reuse existing data/ folder

Docs: https://platform.claude.com/docs/en/build-with-claude/skills-guide
"""

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


# --- 1. synthetic inputs -----------------------------------------------------
def make_synthetic_data() -> list[Path]:
    """Write a fake quarterly-sales CSV plus a notes.md. Returns the paths."""
    DATA_DIR.mkdir(exist_ok=True)
    random.seed(42)
    regions = ["North America", "Europe", "APAC", "LATAM"]
    products = ["Starter", "Pro", "Enterprise"]

    csv_path = DATA_DIR / "sales_2025.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["quarter", "region", "product", "revenue_usd", "new_customers", "churn_pct"])
        for q in range(1, 5):
            for r in regions:
                for p in products:
                    base = {"Starter": 120_000, "Pro": 310_000, "Enterprise": 640_000}[p]
                    growth = 1 + 0.06 * (q - 1) + random.uniform(-0.08, 0.12)
                    w.writerow([
                        f"Q{q}", r, p,
                        round(base * growth),
                        random.randint(15, 140),
                        round(random.uniform(1.5, 6.0), 1),
                    ])

    notes_path = DATA_DIR / "notes.md"
    notes_path.write_text(
        "# Context for the deck\n\n"
        "- Audience: exec team, 10-minute readout.\n"
        "- Story we want: APAC is the growth engine, LATAM churn is the risk.\n"
        "- Brand: dark navy background, white text, one accent color.\n"
        "- Max 6 slides. End with 3 concrete recommendations.\n"
    )
    return [csv_path, notes_path]


# --- 2. agent loop with the pptx skill --------------------------------------
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


# --- 3. pull generated files back --------------------------------------------
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
    inputs = (sorted(DATA_DIR.glob("*")) if "--no-gen" in sys.argv else make_synthetic_data())
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
