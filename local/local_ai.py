from ollama import chat
from pydantic import BaseModel, Field
from typing import List, Literal
import os


class RequirementMatch(BaseModel):
    requirement: str = Field(
        ..., description="Requirement extracted from the job description"
    )
    status: Literal["met", "partial", "missing"] = Field(
        ..., description="How well the CV satisfies this requirement"
    )
    cvEvidence: List[str] = Field(
        default_factory=list,
        description="Exact phrases or items from the CV that support the status",
    )


class JobFitResult(BaseModel):
    fitPercentage: int = Field(
        ..., ge=0, le=100, description="Final fit score from 0 to 100"
    )

    roleFamily: Literal[
        "devops",
        "sre",
        "platform",
        "cloud",
        "backend",
        "systems",
        "other",
    ]

    seniorityRequired: Literal[
        "intern",
        "junior",
        "mid",
        "senior",
        "lead",
    ]

    seniorityCandidate: Literal[
        "intern",
        "junior",
        "mid",
        "senior",
        "lead",
    ]

    mustHaves: List[RequirementMatch] = Field(
        default_factory=list,
        description="Must-have requirements and their match status",
    )

    niceToHaves: List[RequirementMatch] = Field(
        default_factory=list,
        description="Nice-to-have requirements and their match status",
    )

    biggestGaps: List[str] = Field(
        default_factory=list,
        description="Major missing or weak areas affecting the score",
    )

    scoreNotes: List[str] = Field(
        default_factory=list,
        description="Short bullet reasons for penalties, caps, or deductions",
    )


def generate(job, cv):
    MSG = f"""
You are a strict, conservative job-fit evaluator for DevOps/SRE/Platform/Cloud/Infrastructure/Backend/System roles.

Return ONLY a JSON object matching this schema (no extra text):
{{
  "fitPercentage": 0,
  "roleFamily": "devops|sre|platform|cloud|backend|systems|other",
  "seniorityRequired": "intern|junior|mid|senior|lead",
  "seniorityCandidate": "intern|junior|mid|senior|lead",
  "mustHaves": [{{"requirement": "...", "status": "met|partial|missing", "cvEvidence": ["..."]}}],
  "niceToHaves": [{{"requirement": "...", "status": "met|partial|missing", "cvEvidence": ["..."]}}],
  "biggestGaps": ["..."],
  "scoreNotes": ["short bullet reasons for major penalties/caps only"]
}}

Hard rules:
- Do NOT assume skills not explicitly present in the CV.
- A requirement is "met" only if there is direct evidence in the CV (exact term or unambiguous equivalent).
- Be conservative: if unclear, mark "missing".
- If role is primarily outside allowed families, set roleFamily="other" and fitPercentage in 0–25.

Allowed equivalences (do not create new skills):
- k8s == kubernetes
- cicd == jenkins/github actions/gitlab ci (only if named)
- monitoring/observability == prometheus/grafana/loki (only if named)

Scoring method (must follow):
1) Role-family gate: if roleFamily="other" => fitPercentage 0–25.
2) Extract MUST-HAVES, NICE-TO-HAVES, Responsibilities.
3) Weighting:
   - MUST-HAVES 65%, NICE 15%, Responsibilities 10%, Seniority 10%.
4) Seniority caps:
   - Mid required & candidate junior => cap 70
   - Senior required & candidate junior => cap 55
   - Lead required & candidate junior => cap 40
5) Missing critical must-have: subtract 10–25 each based on importance.
6) Final score is an integer 0–100. If unsure, choose the lower.

CV:
{cv}

Job Description:
{job}
"""
    response = chat(
        model=os.getenv("model"),
        stream=False,
        options={"seed": 1, "temperature": 0.2},
        messages=[
            {
                "role": "user",
                "content": MSG,
            }
        ],
        format=JobFitResult.model_json_schema(),
    )
    return response.message.content
