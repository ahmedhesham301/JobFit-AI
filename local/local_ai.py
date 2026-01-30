from ollama import chat
from pydantic import BaseModel
import os

class format(BaseModel):
    fitPercentage: int


def generate(job, cv):
    MSG = f"""Evaluate how well my CV matches the job description.
I'm only interested in backend,devops jobs and anything related to them
Return your answer in the following format:
Fit Percentage (0–100)

my CV:
{cv}

Job Description:
{job}
"""
    response = chat(
        model= os.getenv("model"),
        stream=False,
        options={"seed": 1, "temperature": 0.2},
        messages=[
            {
                "role": "user",
                "content": MSG,
            }
        ],
        format=format.model_json_schema(),
    )
    return response.message.content
