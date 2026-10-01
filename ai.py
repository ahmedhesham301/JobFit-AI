# To run this code you need to install the following dependencies:
# pip install google-genai

from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv("gemini_api_key"))

MODEL = os.getenv("gemini_model")


def create_job_evaluator_cache(system_instruction, cv):
    cache = client.caches.create(
        model=MODEL,
        config=types.CreateCachedContentConfig(
            system_instruction=system_instruction,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=f"""
CANDIDATE CV:

{cv}
""")],
                )
            ],
            display_name="jobfit-evaluator",
            ttl="3600s",  # 1 hour
        ),
    )

    return cache.name


def generate(title, description, cache_name):
    evaluation_input = f"""
JOB TITLE:
{title}

JOB DESCRIPTION:
{description}
"""
    model = MODEL
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=evaluation_input),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="MINIMAL",
        ),
        cached_content=cache_name,
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
                        "growth_potential",
                    ],
                    properties={
                        "skills": genai.types.Schema(
                            type=genai.types.Type.INTEGER,
                            minimum=0,
                            maximum=35,
                        ),
                        "experience": genai.types.Schema(
                            type=genai.types.Type.INTEGER,
                            minimum=0,
                            maximum=30,
                        ),
                        "role_alignment": genai.types.Schema(
                            type=genai.types.Type.INTEGER,
                            minimum=0,
                            maximum=20,
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
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    return response.text


if __name__ == "__main__":
    generate()
