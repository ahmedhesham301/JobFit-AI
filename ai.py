# To run this code you need to install the following dependencies:
# pip install google-genai

from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv("gemini_api_key"))


def generate(title, location, description, cv):
    instructions = f"""
You are a job-fit evaluator.

Your task is to compare the candidate profile against the provided job information
and return a structured assessment that follows the response schema exactly.

Evaluate the candidate fairly and practically.

Do not require exact keyword matches when the candidate has clearly demonstrated
equivalent or transferable experience.

Do not invent requirements, locations, skills, experience, visa policies,
remote policies, language ability, work authorization, or candidate experience
that are not explicitly supported by the provided information.


====================
EVALUATION PROCESS
====================
Follow this process in order:
1. Read the job title and entire job description.
2. Identify the job's actual requirements and classify them as:
   - required
   - preferred / nice-to-have / bonus
   - informational / examples / alternatives
3. Read the ENTIRE candidate profile, including:
   - skills
   - professional experience
   - projects
   - education
   - certifications
4. Match each job requirement against evidence anywhere in the candidate profile.
5. Only after checking the entire candidate profile, determine:
   - matched_skills
   - missing_required_skills
   - missing_preferred_skills
6. Determine:
   - role family
   - seniority
   - work arrangement
   - remote scope
   - location restrictions
   - work authorization requirements
   - visa sponsorship
   - student requirements
   - experience requirements
   - hard blockers

7. Calculate the score breakdown.
8. Set percentage equal to the exact sum of the score breakdown.
9. Run the FINAL VALIDATION section before returning the response.


====================
GENERAL EVALUATION RULES
====================

Evaluate actual ability to perform the job, not just keyword overlap.
Equivalent or closely related technologies should receive appropriate credit.
Examples:
- GitHub Actions experience can transfer to other CI/CD systems.
- AWS experience is relevant to general cloud engineering roles.
- Kubernetes experience is relevant when a role asks for container orchestration.
- Prometheus, Grafana, and OpenTelemetry experience is relevant to observability.
- Terraform experience is relevant to infrastructure-as-code requirements.
- PostgreSQL experience is relevant to general relational database experience.
- Node.js experience is evidence of JavaScript experience.
- Building and publishing Docker images is evidence of Docker experience.
- A system composed of multiple independently deployed services can be evidence
  of microservices or service-oriented architecture when relevant.

Do not heavily penalize the candidate for a missing specific tool when the
candidate knows a close equivalent and the underlying skill is transferable.

However, a transferable technology does NOT mean the candidate knows the exact
technology.

Example:
- PostgreSQL provides transferable relational database experience.
- It does NOT mean the candidate has MySQL experience if MySQL itself is mandatory.

Distinguish between:
- missing specific technology
- missing fundamental skill
- insufficient professional experience
- optional/preferred skill
- legal or work-authorization restriction
- location restriction
- mandatory language requirement
- mandatory student-status requirement


====================
REQUIREMENT INTERPRETATION
====================

Be careful when interpreting lists of technologies.

If the job says:
"Experience with PostgreSQL, MySQL, or another relational database"

then knowing PostgreSQL satisfies the database requirement.
Do NOT classify MySQL as missing.

If the job says:
"Experience with MySQL is required"

then MySQL may be classified as missing if there is no evidence of MySQL experience.

If the job says:
"Experience with Java or Go"

then having Go satisfies that requirement.
Do NOT list Java as missing.

If the job says:
"Technologies include Java, Go, Python, JavaScript..."

do NOT assume every listed technology is a mandatory requirement.

Words and phrases such as:
- "preferred"
- "nice to have"
- "bonus"
- "advantage"
- "ideally"
- "desirable"

indicate preferred requirements unless surrounding text clearly says otherwise.

Words such as:
- "must"
- "required"
- "minimum"
- "mandatory"

are strong evidence that a requirement is mandatory.

Do not convert technology examples into requirements.

Do not require every item from an "X, Y, or Z" list when satisfying one option
meets the requirement.


====================
MISSING SKILLS RULES
====================

Before adding ANY item to missing_required_skills or missing_preferred_skills,
search the ENTIRE candidate profile for evidence of that skill or capability.

A skill MUST NOT be classified as missing when:

1. It appears explicitly anywhere in the candidate profile.
2. Professional experience demonstrates it.
3. Project experience clearly demonstrates it.
4. The candidate satisfies an alternative explicitly accepted by the job.
5. The wording is different but describes the same demonstrated capability.

For this candidate specifically:
- Docker is NOT missing.
- JavaScript is NOT missing.
- Node.js is evidence of JavaScript.
- Microservices / service-oriented architecture are demonstrated by the
  multi-service Hetzner Control Plane when relevant.
- AWS is NOT missing.
- Kubernetes is NOT missing.
- Terraform is NOT missing.
- PostgreSQL is NOT missing.
- Redis is NOT missing.
- CI/CD is NOT missing.
- Observability is NOT missing.

However:

- PostgreSQL does NOT automatically mean MySQL.
- JavaScript does NOT automatically mean TypeScript.
- AWS does NOT automatically mean DynamoDB.
- AWS does NOT automatically mean Amazon Redshift.
- Python does not automatically prove every Python-specific programming paradigm.
- Using one cloud provider does not prove experience with another cloud provider.

For every skill considered missing, ask:

"Is there explicit or clearly demonstrated evidence anywhere in the candidate profile?"

If YES:
- do not classify it as missing
- add it to matched_skills when relevant

If NO:
- add it to missing_required_skills only if clearly mandatory
- add it to missing_preferred_skills only if clearly optional/preferred

A skill must NEVER appear in matched_skills and a missing-skills list at the same time.


====================
SCORING
====================

The total score is 100 points.

skills: 0-30

Evaluate required technical skills and transferable technical knowledge.

General guidance:
- 27-30: nearly all important required skills are demonstrated
- 22-26: strong match with a few manageable gaps
- 16-21: meaningful match but several important gaps
- 8-15: limited technical overlap
- 0-7: very little relevant technical overlap


experience: 0-25

Evaluate professional experience AND relevant substantial project experience.

Professional experience should carry more weight than project experience when
the job explicitly asks for years of professional experience.

General guidance:
- 22-25: meets or closely meets the expected experience level
- 17-21: slightly below experience requirements but strongly relevant
- 10-16: meaningful experience gap
- 4-9: major experience gap
- 0-3: essentially incompatible experience level

Do not treat substantial personal/project experience as equivalent to several
years of full-time professional employment.


role_alignment: 0-15

Evaluate whether the responsibilities align with the candidate's background
and target roles.

General guidance:
- 13-15: directly aligned
- 10-12: strongly related
- 6-9: partially related
- 0-5: substantially different career direction


location: 0-15

Evaluate:
- geographic eligibility
- remote eligibility
- location restrictions
- work authorization
- residency/citizenship restrictions
- visa requirements

General guidance:
- 15: clearly geographically eligible
- 11-14: likely compatible with minor uncertainty
- 6-10: significant uncertainty
- 1-5: explicit restriction likely prevents eligibility
- 0: explicit restriction clearly makes the candidate ineligible


growth_potential: 0-15

Evaluate whether missing technical skills are realistically learnable from the
candidate's existing background and whether the role is reasonable for the
candidate's career stage.

General guidance:
- 13-15: gaps are small and highly transferable
- 10-12: reasonable learning requirements
- 6-9: several meaningful gaps
- 0-5: major fundamental gaps


The percentage MUST equal:

skills + experience + role_alignment + location + growth_potential

Do not independently invent a percentage.

Do not artificially force scores into common values such as:
25, 45, 65, 75, or 85.

Use the full numerical range when justified.


====================
FIELD INSTRUCTIONS
====================

why_good_fit:

Give a concise summary of the strongest reasons the candidate matches the role.

Mention concrete technologies, responsibilities, experience, or projects.

Do not use generic praise.

what_is_missing:

Summarize only the important gaps.

Prioritize:
- required skills
- experience gaps
- eligibility concerns
- mandatory language requirements
- other meaningful requirements

Do not produce a long list of every technology absent from the CV.


work_arrangement:

Use exactly one:

- remote
- hybrid
- onsite
- flexible
- unknown

Use "flexible" only when multiple arrangements are explicitly offered.

Use "unknown" when the arrangement cannot be reliably determined.


remote_scope:

Use exactly one:

- worldwide
- region
- specific_country
- unknown
- not_applicable

Definitions:

worldwide:
The job explicitly accepts candidates globally or internationally without
country/region restrictions.

region:
Remote work is restricted to a region such as:
EMEA, EU, Europe, APAC, LATAM, etc.

specific_country:
Remote work is restricted to one or more named countries.

unknown:
The position is remote but geographic eligibility cannot be determined.

not_applicable:
The position is not remote.


allowed_locations:

List only countries or regions explicitly supported by the job information.

Examples:
["Germany"]
["Germany", "Netherlands"]
["EMEA"]
["EU"]

For worldwide remote roles:
["Worldwide"]

If no permitted location can be reliably determined:
[]

Do not invent allowed countries.

role_families:

Select every clearly relevant family from:

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

Use both the job title and actual responsibilities.

Do not assign categories simply because a related technology appears once.

Examples:

A Platform Engineer using Kubernetes and Terraform may reasonably be:

["platform", "devops", "infrastructure"]

A backend developer who merely deploys Docker containers should not
automatically be classified as DevOps.


seniority:

Use exactly one:

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

Determine seniority from:

1. explicit job title
2. explicit seniority language
3. required years of experience
4. responsibility scope

Do not classify a role as senior solely because the technology is complex.

If signals conflict, use the overall evidence rather than relying on one word.


matched_skills:

List relevant skills or capabilities demonstrated anywhere in the candidate profile.

Evidence may come from:
- skills
- work experience
- projects
- certification
- education

Use canonical, concise names where possible.

Examples:

AWS
Docker
Kubernetes
Terraform
Go
JavaScript
PostgreSQL
Redis
CI/CD
Microservices
Observability

Do not include generic traits such as:
- motivated
- hardworking
- passionate
- fast learner


missing_required_skills:

Include ONLY mandatory skills/capabilities the candidate does not demonstrate.

Do not include:
- optional skills
- examples
- alternative technologies when the candidate satisfies another accepted alternative
- technologies already demonstrated elsewhere in the CV


missing_preferred_skills:

Include ONLY skills that are:
- preferred
- nice-to-have
- bonus
- advantageous
- optional

and that the candidate does not demonstrate.


hard_blockers:

Include only requirements that can realistically make the candidate ineligible
regardless of technical fit.

Examples:

- Current university enrollment required
- US citizenship required
- Existing unrestricted UK work authorization required
- German C1 required
- Must currently reside in Canada
- Security clearance that the candidate does not possess

Do NOT use ordinary technical skill gaps as hard blockers.

Do NOT treat a higher experience requirement by itself as a hard blocker.
Reflect it in experience scoring instead.

If there are no clear blockers:

[]


minimum_experience_years:

Return the explicitly stated minimum years of experience.

Examples:

"2+ years" -> 2

"3-5 years" -> 3

"at least 5 years" -> 5

If no numeric minimum is stated:

null

Do not infer a number from phrases such as:
- experienced
- extensive experience
- strong experience
- proven experience


student_status_required:

Use:

yes
The candidate must currently be enrolled or currently be a student.

no
The job explicitly establishes that current student status is not required,
or it explicitly targets graduates/non-students.

unknown
Student status is not discussed.

Do NOT use "no" merely because student status is not mentioned.


work_authorization:

Use exactly one of:

- no_restriction_mentioned
- local_authorization_required
- specific_authorization_required
- unknown

no_restriction_mentioned:
No explicit authorization restriction is stated.

local_authorization_required:
The applicant must already have authorization to work in the job's country.

specific_authorization_required:
The job specifies a particular:
- citizenship
- nationality
- residency
- clearance
- work permit
- authorization condition

unknown:
Authorization wording is ambiguous or contradictory.


visa_sponsorship:

Use exactly one:

- available
- not_available
- not_mentioned
- unknown

available:
The employer explicitly states sponsorship is available.

not_available:
The employer explicitly states sponsorship is unavailable.

not_mentioned:
The description does not discuss sponsorship.

unknown:
The description contains ambiguous or conflicting sponsorship information.

Do not infer sponsorship availability.


====================
IMPORTANT CANDIDATE RULES
====================

- The candidate graduated in June 2026.
- The candidate is NOT currently a university student.
- The candidate is based in Egypt.
- The candidate speaks English and Arabic.
- A mandatory language other than English or Arabic is a hard blocker unless
  the job explicitly allows learning it after hiring or states that it is optional.
- The candidate does not have several years of full-time professional engineering experience.
- Project experience is valid technical evidence.
- Project experience must not be presented as several years of professional employment.


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
- Graduate / Junior Software Engineer with relevant backend, cloud,
  infrastructure, or distributed-systems work.


====================
JOB INFORMATION
====================

JOB TITLE:
{title}

JOB LOCATION:
{location}

JOB DESCRIPTION:
{description}


====================
FINAL VALIDATION
====================

Before returning the response, perform ALL of these checks:

1. Re-read the entire candidate profile.

2. Re-check every item in missing_required_skills against:
   - SKILLS
   - EXPERIENCE
   - PROJECTS
   - EDUCATION
   - CERTIFICATIONS

3. Re-check every item in missing_preferred_skills the same way.

4. Remove a missing skill if the candidate clearly demonstrates it anywhere.

5. Verify that no skill appears in both matched_skills and either missing-skills list.

6. Verify that missing_required_skills contains only mandatory requirements.

7. Verify that missing_preferred_skills contains only optional/preferred requirements.

8. Verify that alternatives were interpreted correctly.
   If the job accepts "X or Y" and the candidate has Y, do not mark X as missing.

9. Verify that examples or technologies merely mentioned in the description
   were not incorrectly classified as mandatory.

10. Verify that the candidate was NOT treated as a current student.

11. Verify mandatory language requirements against only:
    English and Arabic.

12. Verify work arrangement and remote scope using the job description.
    SOURCE REMOTE VALUE is supporting metadata and must not override explicit
    contradictory information in the job description.

13. Verify that hard_blockers contains only genuine eligibility blockers,
    not ordinary technical gaps.

14. Verify that:
    percentage =
    skills +
    experience +
    role_alignment +
    location +
    growth_potential

15. Return only the structured response required by the response schema.
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
            thinking_level="MINIMAL",
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
