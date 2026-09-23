# To run this code you need to install the following dependencies:
# pip install google-genai

from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv("gemini_api_key"))


def generate(title, location, description, cv):
    instructions = f"""You are evaluating a job listing for a me. Score how suitable the job is for the me from 0-100.
Focus primarily on whether the I could realistically perform the job, not whether my background is an exact match.
SCORING:
* Skills and responsibilities match: 0-40
* Experience/seniority match: 0-20
* Transferable skills and ability to learn missing technologies: 0-20
* Role/career relevance: 0-15
* Location/remote alignment: 0-5
Give credit for equivalent or transferable technologies. Do not heavily penalize missing tools that could reasonably be learned if the candidate has related experience.
Major penalties should mainly apply when:
* The role is unrelated to the candidate's career direction
* Seniority is far above the candidate's experience
* A core required skill is missing with no transferable experience
* A mandatory location/work-authorization requirement cannot be met

cv:
    {cv}
"""

    job_info = f"""
    job title: {title}
    job location: {location}
    job description:
    {description}"""
    model = "gemini-2.5-flash"
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
            thinking_budget=0,
        ),
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            required=[
                "percentage",
                "why I'm I a good fit in summary",
                "what I'm I missing in summary",
            ],
            properties={
                "percentage": genai.types.Schema(
                    type=genai.types.Type.INTEGER,
                ),
                "why I'm I a good fit in summary": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "what I'm I missing in summary": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
            },
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
