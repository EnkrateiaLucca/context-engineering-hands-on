from pydantic import BaseModel
from anthropic import Anthropic


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
    model="claude-sonnet-4-6",
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