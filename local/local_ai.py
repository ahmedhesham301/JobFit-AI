from ollama import chat
from pydantic import BaseModel
import os

class format(BaseModel):
    fitPercentage: int


def generate(job, cv):
    MSG = f"""You are a strict job-fit evaluator for DevOps/backend roles.
Score how well the CV matches this job description.

Rules:
- Only DevOps/SRE/Platform/Cloud/Infrastructure/Backend/Systems roles are relevant.
- If the role is primarily frontend, data/ML, sales, marketing, support, PM, design, finance, etc., score 0–25.
- Do not assume skills not explicitly in the CV.
- Penalize missing must‑have requirements or seniority mismatch (e.g., lead/principal with many years).
- Be conservative; if unsure, choose the lower score.

Scoring rubric (0-100):
- 0-25: Not relevant / different job family
- 26-50: Partially related but major gaps or different focus
- 51-70: Reasonable match with some gaps
- 71-85: Strong match; most requirements met
- 86-100: Excellent match; nearly all requirements met and level aligns

Return ONLY a JSON object that matches this schema:
{{"fitPercentage": 0}}

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
