# To run this code you need to install the following dependencies:
# pip install google-genai

from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv("gemini_api_key"))


def generate(title, location, description, cv):
    instructions = f"""You are a job-fit evaluator.

Your task is to compare the candidate profile against the provided job description and return a structured assessment that follows the response schema exactly.

Evaluate the candidate fairly and practically. Do not require an exact keyword match when the candidate has clearly transferable or equivalent experience.

Do not invent requirements, locations, skills, experience, visa policies, remote policies, or candidate experience that are not explicitly supported by the provided information.

====================
CANDIDATE PROFILE
====================

{cv}

Primary target roles:
- Backend Engineer
- Go Backend Engineer
- DevOps Engineer
- Platform Engineer
- Cloud Engineer
- Site Reliability Engineer
- Infrastructure Engineer
- Graduate / Junior Software Engineer with relevant backend, cloud, infrastructure, or distributed-systems work.

Important candidate facts:
- The candidate graduated in June 2026.
- Do NOT treat the candidate as a current university student.
- The candidate is based in Egypt.
- The candidate only speaks English and Arabic
- The candidate does not have several years of full-time professional engineering experience.
- Project experience is valid technical experience, but it should not be presented as equivalent to several years of professional employment.

====================
JOB INFORMATION
====================
JOB TITLE:
{title}

JOB DESCRIPTION:
{description}

====================
EVALUATION RULES
====================

Evaluate actual ability to perform the job, not just exact keyword overlap.

Equivalent or closely related technologies should receive partial or full credit when appropriate.

Examples:
- GitHub Actions experience can transfer to other CI/CD systems.
- AWS experience is relevant to general cloud engineering roles.
- Kubernetes experience is relevant when a role asks for container orchestration.
- Prometheus/Grafana/OpenTelemetry experience is relevant to observability requirements.
- Terraform experience is relevant to infrastructure-as-code requirements even if another IaC tool is preferred.
- PostgreSQL experience is relevant to relational database requirements.

Do not heavily penalize the candidate for a missing tool if they already know a close equivalent.

However, do distinguish between:
- a missing tool,
- a missing fundamental skill,
- insufficient professional experience,
- a legal/location restriction,
- a mandatory language requirement,
- and a mandatory educational/student-status requirement.

A "preferred", "nice to have", "bonus", or similar skill must NOT be treated as a required skill.

====================
SCORING
====================

The total score is 100 points.

skills: 0-30
Evaluate how well the candidate's technical skills match required job skills.

experience: 0-25
Evaluate professional and relevant project experience against the role's experience requirements.

role_alignment: 0-15
Evaluate whether the candidate's background and target career direction align with the actual responsibilities.

location: 0-15
Evaluate geographic eligibility, remote eligibility, work authorization requirements, and relevant location restrictions.

growth_potential: 0-15
Evaluate whether missing skills are realistically learnable given the candidate's existing background and whether the role is reasonable for their career stage.

The `percentage` MUST equal:

skills + experience + role_alignment + location + growth_potential

Do not independently invent a percentage that conflicts with the score breakdown.

Do not artificially force scores into fixed buckets such as 25, 45, 65, or 85.
Use the full available score range when justified.

====================
FIELD INSTRUCTIONS
====================

why_good_fit:
Give a concise summary of the strongest reasons the candidate matches the job.
Mention concrete matching technologies, responsibilities, or experience.
Do not use generic praise.

what_is_missing:
Summarize the most important gaps.
Focus on meaningful requirements rather than listing every technology that is not on the CV.

work_arrangement:
Use exactly one of:
- remote
- hybrid
- onsite
- flexible
- unknown

Use "flexible" only when the job explicitly supports multiple work arrangements.

remote_scope:
Use exactly one of:
- worldwide
- region
- specific_country
- unknown
- not_applicable

Rules:
- worldwide: explicitly open internationally/worldwide.
- region: remote work is restricted to a region such as EMEA, EU, Europe, APAC, etc.
- specific_country: remote work is restricted to one or more specified countries.
- unknown: the role is remote but geographic eligibility is not clear.
- not_applicable: the role is not remote.

allowed_locations:
List the countries or regions where the candidate may work according to the job description.

Examples:
["Germany"]
["Germany", "Netherlands"]
["EMEA"]
["EU"]

For worldwide remote roles:
["Worldwide"]

If no permitted location can be determined:
[]

Do not infer countries that are not stated.

role_families:
Select every clearly relevant role family.

Allowed values:
- backend
- devops
- platform
- sre
- cloud
- infrastructure
- sysadmin
- software_engineering
- security
- data
- ai_ml
- networking
- other

Do not assign every remotely related category.
Choose only meaningful role families.

seniority:
Use exactly one of:
- intern
- working_student
- graduate
- entry_level
- junior
- mid
- senior
- lead
- manager
- director
- unknown

Determine seniority primarily from explicit title and experience requirements.

Do not classify a job as senior merely because it has challenging technical requirements.

matched_skills:
Return concrete skills or technologies from the candidate profile that meaningfully match the job.

Do not include generic qualities such as:
- motivated
- hardworking
- passionate
- fast learner

missing_required_skills:
Include only skills or technologies that the job clearly treats as mandatory and which the candidate does not demonstrate.

missing_preferred_skills:
Include missing "preferred", "nice-to-have", "bonus", or optional skills.

Do not mix required and preferred skills.

hard_blockers:
Include only requirements that can realistically make the candidate ineligible regardless of technical fit.

Examples:
- "Must currently be enrolled at a university"
- "US citizenship required"
- "Must already have unrestricted UK work authorization"
- "German C1 required"
- "Role is only open to candidates located in Canada"

Do NOT use minor skill gaps as hard blockers.

If there are no clear hard blockers:
[]

minimum_experience_years:
Return the minimum explicitly required number of years.

Examples:
"2+ years" -> 2
"3-5 years" -> 3
"at least 5 years" -> 5

If no numeric minimum is given:
null

Do not estimate a number from terms such as "experienced" or "strong experience."

student_status_required:
Use:
- yes: the candidate must currently be enrolled/a student.
- no: the description explicitly establishes that student status is not required or specifically targets graduates/non-students.
- unknown: student status is not discussed.

Do NOT automatically use "no" merely because the job does not mention students.

work_authorization:
Use exactly one of:
- no_restriction_mentioned
- local_authorization_required
- specific_authorization_required
- unknown

Definitions:

no_restriction_mentioned:
The job contains no explicit work-authorization restriction.

local_authorization_required:
The applicant must already have permission to work in the job's country.

specific_authorization_required:
The description specifies a particular citizenship, residency, security clearance, nationality, or authorization condition.

unknown:
The wording is ambiguous or contradictory.

visa_sponsorship:
Use:
- available
- not_available
- not_mentioned
- unknown

Do not assume visa sponsorship is available simply because the job is international.

Use "not_mentioned" when sponsorship is not discussed.

Use "unknown" only when the description contains ambiguous or conflicting sponsorship information.

====================
IMPORTANT RULES
====================

1. Base the assessment only on the candidate profile and job description.

2. Do not invent candidate skills.

3. Do not assume that a technology is known simply because it is similar to one the candidate knows. Transferability can increase the score, but the missing skill should still be identified when it is explicitly required.

4. Do not treat preferred requirements as mandatory.

5. Do not assume work authorization, visa sponsorship, or geographic eligibility unless the job description states it.

6. Do not assume the candidate is currently a student. The candidate graduated in June 2026.

7. If a role requires current student status, add it to hard_blockers and set student_status_required to "yes".

8. If a job requires substantially more professional experience than the candidate has, reduce the experience score appropriately even if technical skills match well.

9. A hard blocker does not erase technical fit. Continue scoring skills and role alignment accurately, while reflecting the blocker strongly in the location/eligibility-related assessment.

10. Be generous about realistic skill transfer, but strict about legal, geographic, language, student-status, clearance, and mandatory experience restrictions.

11. Keep why_good_fit and what_is_missing concise.

12. Return only information supported by the provided candidate profile and job description.
"""

    job_info = f"""
job title: {title}
job location: {location}
job description:
{description}"""
    model = "gemini-3.5-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=job_info),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="LOW",
        ),
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            required=[
                "percentage",
                "why_good_fit",
                "what_is_missing",
                "work_arrangement",
                "remote_scope",
                "allowed_locations",
                "role_families",
                "seniority",
                "matched_skills",
                "missing_required_skills",
                "missing_preferred_skills",
                "hard_blockers",
                "minimum_experience_years",
                "student_status_required",
                "work_authorization",
                "visa_sponsorship",
                "score_breakdown",
            ],
            properties={
                "percentage": genai.types.Schema(
                    type=genai.types.Type.INTEGER,
                    minimum=0,
                    maximum=100,
                ),
                "why_good_fit": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "what_is_missing": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "work_arrangement": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    enum=[
                        "remote",
                        "hybrid",
                        "onsite",
                        "flexible",
                        "unknown",
                    ],
                ),
                "remote_scope": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    enum=[
                        "worldwide",
                        "region",
                        "specific_country",
                        "unknown",
                        "not_applicable",
                    ],
                ),
                "allowed_locations": genai.types.Schema(
                    type=genai.types.Type.ARRAY,
                    items=genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                ),
                "role_families": genai.types.Schema(
                    type=genai.types.Type.ARRAY,
                    items=genai.types.Schema(
                        type=genai.types.Type.STRING,
                        enum=[
                            "backend",
                            "devops",
                            "platform",
                            "sre",
                            "cloud",
                            "infrastructure",
                            "sysadmin",
                            "software_engineering",
                            "security",
                            "data",
                            "ai_ml",
                            "networking",
                            "other",
                        ],
                    ),
                ),
                "seniority": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    enum=[
                        "intern",
                        "working_student",
                        "graduate",
                        "entry_level",
                        "junior",
                        "mid",
                        "senior",
                        "lead",
                        "manager",
                        "director",
                        "unknown",
                    ],
                ),
                "matched_skills": genai.types.Schema(
                    type=genai.types.Type.ARRAY,
                    items=genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                ),
                "missing_required_skills": genai.types.Schema(
                    type=genai.types.Type.ARRAY,
                    items=genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                ),
                "missing_preferred_skills": genai.types.Schema(
                    type=genai.types.Type.ARRAY,
                    items=genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                ),
                "hard_blockers": genai.types.Schema(
                    type=genai.types.Type.ARRAY,
                    items=genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                ),
                "minimum_experience_years": genai.types.Schema(
                    type=genai.types.Type.INTEGER,
                    minimum=0,
                    nullable=True,
                ),
                "student_status_required": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    enum=[
                        "yes",
                        "no",
                        "unknown",
                    ],
                ),
                "work_authorization": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    enum=[
                        "no_restriction_mentioned",
                        "local_authorization_required",
                        "specific_authorization_required",
                        "unknown",
                    ],
                ),
                "visa_sponsorship": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    enum=[
                        "available",
                        "not_available",
                        "not_mentioned",
                        "unknown",
                    ],
                ),
                "score_breakdown": genai.types.Schema(
                    type=genai.types.Type.OBJECT,
                    required=[
                        "skills",
                        "experience",
                        "role_alignment",
                        "location",
                        "growth_potential",
                    ],
                    properties={
                        "skills": genai.types.Schema(
                            type=genai.types.Type.INTEGER,
                            minimum=0,
                            maximum=30,
                        ),
                        "experience": genai.types.Schema(
                            type=genai.types.Type.INTEGER,
                            minimum=0,
                            maximum=25,
                        ),
                        "role_alignment": genai.types.Schema(
                            type=genai.types.Type.INTEGER,
                            minimum=0,
                            maximum=15,
                        ),
                        "location": genai.types.Schema(
                            type=genai.types.Type.INTEGER,
                            minimum=0,
                            maximum=15,
                        ),
                        "growth_potential": genai.types.Schema(
                            type=genai.types.Type.INTEGER,
                            minimum=0,
                            maximum=15,
                        ),
                    },
                    property_ordering=[
                        "skills",
                        "experience",
                        "role_alignment",
                        "location",
                        "growth_potential",
                    ],
                ),
            },
            property_ordering=[
                "percentage",
                "why_good_fit",
                "what_is_missing",
                "work_arrangement",
                "remote_scope",
                "allowed_locations",
                "role_families",
                "seniority",
                "matched_skills",
                "missing_required_skills",
                "missing_preferred_skills",
                "hard_blockers",
                "minimum_experience_years",
                "student_status_required",
                "work_authorization",
                "visa_sponsorship",
                "score_breakdown",
            ],
        ),
        system_instruction=[
            types.Part.from_text(text=instructions),
        ],
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    return response.text


if __name__ == "__main__":
    generate()
