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

You MUST return ONLY a JSON object that conforms to the provided schema via the tool format.
No prose. No markdown. No extra keys.

CRITICAL RULES (anti-hallucination):
- Do NOT assume skills not explicitly present in the CV.
- Do NOT invent requirements. Every requirement in mustHaves/niceToHaves MUST be grounded in the Job Description.
  - For each requirement, copy a short phrase from the JD (verbatim or near-verbatim).
- Evidence-first: Before marking ANY requirement as "missing", scan the CV for relevant keywords/synonyms.
  If you find explicit evidence, it cannot be "missing".
- Consistency:
  - If status is "met" or "partial", cvEvidence MUST contain 1+ exact CV snippets.
  - If cvEvidence is empty, status MUST be "missing".

ROLE-FAMILY GATE (very important):
- First decide the job family based on the JD’s core responsibilities and required tools.
- If the JD is primarily outside DevOps/SRE/Platform/Cloud/Infra/Backend/Systems
  (examples: seismic geophysics, sales enablement admin, finance, marketing, HR, design, PM, support),
  set roleFamily="other" and fitPercentage MUST be between 0 and 25.

ALLOWED EQUIVALENCES (do not create new skills):
- k8s == kubernetes
- cicd == jenkins/github actions/gitlab ci (only if named)
- monitoring/observability == prometheus/grafana/loki (only if named)

REQUIREMENT EXTRACTION:
1) Extract MUST-HAVES only if JD uses signals like: "must", "required", "minimum", "need", "strong experience".
2) Extract NICE-TO-HAVES if JD uses: "preferred", "plus", "nice to have".
3) IMPORTANT: If a JD bullet contains multiple skills (e.g., AWS + Docker + ECS),
   split it into 2–4 atomic requirements so matching is accurate.

MATCHING LOGIC:
- status="met": clear direct CV evidence matches the requirement.
- status="partial": CV matches a meaningful subset of a compound requirement OR evidence is weaker/less complete.
- status="missing": no explicit evidence in CV.

SENIORITY:
- Infer seniorityRequired from JD (years, "senior/lead/principal", ownership).
- Infer seniorityCandidate from CV (internships/student => intern/junior).
- Apply caps:
  - Mid required & candidate junior/intern => cap 70
  - Senior required & candidate junior/intern => cap 55
  - Lead required & candidate junior/intern => cap 40

SCORING:
- MUST-HAVES 65%, NICE 15%, Responsibilities 10%, Seniority 10%.
- Missing critical must-have: subtract 10–25 depending on importance.
- Choose the LOWER score if uncertain.

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
