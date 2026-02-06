from ollama import chat
from pydantic import BaseModel
import os

class format(BaseModel):
    fitPercentage: int


def generate(job, cv):
    MSG = f"""
You are a strict, conservative job-fit evaluator for DevOps/SRE/Platform/Cloud/Infrastructure/Backend/System roles.

Your task:
- Compare the CV to the Job Description.
- Do the evaluation steps internally.
- Output ONLY a JSON object: {{"fitPercentage": <0-100 integer>}} with no extra keys/text.

Hard rules:
- Do NOT assume skills not explicitly present in the CV.
- Count a requirement as met ONLY if there is direct evidence in the CV (exact term or unambiguous equivalent).
- Be conservative: if evidence is weak/unclear, treat as NOT met.
- Penalize missing MUST-HAVES heavily.
- Penalize seniority mismatch heavily (junior vs senior/lead/principal).
- If role is primarily NOT in the allowed families (frontend, data/ML, sales, marketing, support, PM, design, finance), score 0–25.

Normalization / synonyms (allowed only as equivalents, not as new skills):
- k8s == kubernetes
- iac == terraform/ansible/cloudformation (only if named)
- cicd == jenkins/github actions/gitlab ci (only if named)
- observability/monitoring == prometheus/grafana/loki (only if named)
- aws services only count if explicitly listed (e.g., EC2, RDS, IAM)

Evaluation procedure (do NOT output these steps, only use them to decide):
1) Role-family gate (0–25 if not DevOps/SRE/Platform/Cloud/Infra/Backend/Systems).
2) Determine seniority level required from JD:
   - Intern/Junior/Entry: 0–2 yrs
   - Mid: 2–5 yrs
   - Senior: 5–8 yrs
   - Staff/Lead/Principal: 8+ yrs or leadership ownership
   Infer candidate level from CV dates/titles (internships/student => Junior/Entry).
3) Extract requirements from JD into:
   - MUST-HAVE requirements (keywords like “must”, “required”, “minimum”, “need”)
   - NICE-TO-HAVE requirements (keywords like “preferred”, “plus”, “nice”)
   - Core responsibilities (what they will do day-to-day)
4) Match CV evidence to each requirement:
   - Mark as Met / Partially Met / Not Met.
   - Only Met if explicit.
5) Score with weights:
   - MUST-HAVES: 65%
   - NICE-TO-HAVES: 15%
   - Responsibilities alignment: 10%
   - Seniority alignment: 10%
6) Apply caps/penalties:
   - If any critical MUST-HAVE missing, subtract 10–25 each depending on importance.
   - If JD requires Mid (2–5 yrs) and candidate is Junior, cap at 70.
   - If JD requires Senior (5+ yrs) and candidate is Junior, cap at 55.
   - If JD requires Lead/Principal and candidate is Junior, cap at 40.
   - If JD requires a specific cloud (AWS/GCP/Azure) and CV lacks that cloud, subtract 20.
7) Convert to final integer 0–100 using the rubric below, choosing the LOWER score if uncertain.

Rubric anchors:
- 0–25: Not relevant / different job family
- 26–50: Partially related but major gaps or different focus
- 51–70: Reasonable match with some gaps
- 71–85: Strong match; most requirements met
- 86–100: Excellent match; nearly all requirements met and level aligns

Now evaluate.

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
