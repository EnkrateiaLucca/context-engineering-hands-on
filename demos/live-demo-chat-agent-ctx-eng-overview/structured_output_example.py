# /// script
# requires-python = ">=3.12"
# dependencies = ["anthropic", "pydantic", "python-dotenv"]
# ///
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class Quiz(BaseModel):
    questions: list[str]
    answers: list[str]


client = Anthropic()


user_input = """
Create a quiz about the basics of Python
for building personal automations.
3 questions.
"""

response = client.messages.parse(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": user_input,
        }
    ],
    output_format=Quiz,
)

print(response.parsed_output)