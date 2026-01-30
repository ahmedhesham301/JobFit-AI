from ollama import chat
from pydantic import BaseModel
import os

class format(BaseModel):
    fitPercentage: int


def generate(job, cv):
    MSG = f"""
You are a technical recruiter and hiring manager.

Task:
Evaluate how well my CV matches the job description.

Return your answer in the following format:
Fit Percentage (0–100)

Rules:
- Be strict and realistic.
- Base the evaluation only on the information provided.
- Do not assume missing skills or experience.

CV:
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
