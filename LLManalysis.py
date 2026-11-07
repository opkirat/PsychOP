import json
from typing import List, Literal

from google import genai
from pydantic import BaseModel, Field

from clean_data import sort_by_date

data = sort_by_date[:100]

## Necessary Output Structure
class Message(BaseModel):
    sender: Literal["Me", "Dubey"]
    text: str

class TrainingExample(BaseModel):
    context: list[Message]
    input: list[str]
    output: list[str]

class TrainingDataset(BaseModel):
    examples: list[TrainingExample]



prompt = f"""
You are preprocessing a chronological text message conversation
between "Me" and "Dubey". No calcutions.

Your task is to construct training examples for predicting
Dubey's next response to Me.

Instructions:
1. Messages are already sorted chronologically. Preserve their order.
2. Group consecutive messages from the same sender into bursts.
3. Create one training example whenever a burst from "Me"
   is immediately followed by a burst from "Dubey".
4. Input: all messages in Me's burst.
5. Output: all messages in Dubey's following burst.
6. Context: up to 20 individual messages preceding the input,
   including messages from both participants.
7. Context must exclude the current input and output.
8. Preserve all message text exactly, including spelling,
   punctuation, slang, capitalization, and emojis.
9. Never invent, rewrite, summarize, or merge individual messages.
10. Exclude examples without a completed Dubey response.
11. Treat gaps exceeding 6 hours as session boundaries.
12. Do not create examples crossing session boundaries.

Conversation data:
{json.dumps(data, ensure_ascii=False, default=str)}
"""


client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input = prompt,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": TrainingDataset.model_json_schema()
    },
)

dataset = TrainingDataset.model_validate_json(interaction.output_text)
print(dataset)


## Save the training data
with open("training_data.json", "w", encoding="utf-8") as f:
        json.dump(
        dataset.model_dump(),
        f,
        indent=2,
        ensure_ascii=False
    )