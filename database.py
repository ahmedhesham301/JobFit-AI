import json
import os
import sqlite3
from contextlib import contextmanager

import pandas as pd

from utils import hash_text

data_path = os.getenv("data_path")
# Bump these when changing the evaluation instructions or profile interpretation.
PROMPT_VERSION = 4
CANDIDATE_PROFILE_VERSION = 1

SCHEMA = """
CREATE TABLE IF NOT EXISTS descriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    description_hash TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Hash of everything that affects the AI evaluation:
    -- title + description_hash + location/country + remote metadata
    -- + prompt version + candidate profile version
    evaluation_hash TEXT UNIQUE NOT NULL,

    description_id INTEGER NOT NULL,

    -- Overall result
    why_good_fit TEXT NOT NULL,
    what_missing TEXT NOT NULL,

    percentage INTEGER NOT NULL
        CHECK (percentage BETWEEN 0 AND 100),

    -- Job classification
    work_arrangement TEXT NOT NULL
        CHECK (
            work_arrangement IN (
                'remote',
                'hybrid',
                'onsite',
                'flexible',
                'unknown'
            )
        ),

    remote_scope TEXT NOT NULL
        CHECK (
            remote_scope IN (
                'worldwide',
                'region',
                'specific_country',
                'unknown',
                'not_applicable'
            )
        ),

    seniority TEXT NOT NULL
        CHECK (
            seniority IN (
                'intern',
                'working_student',
                'graduate',
                'entry_level',
                'junior',
                'mid',
                'senior',
                'lead',
                'manager',
                'director',
                'unknown'
            )
        ),

    -- JSON arrays
    allowed_locations TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(allowed_locations)),

    role_families TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(role_families)),

    matched_skills TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(matched_skills)),

    missing_required_skills TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(missing_required_skills)),

    missing_preferred_skills TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(missing_preferred_skills)),

    hard_blockers TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(hard_blockers)),

    -- Requirements
    minimum_experience_years INTEGER
        CHECK (
            minimum_experience_years IS NULL
            OR minimum_experience_years >= 0
        ),

    student_status_required TEXT NOT NULL
        CHECK (
            student_status_required IN (
                'yes',
                'no',
                'unknown'
            )
        ),

    work_authorization TEXT NOT NULL
        CHECK (
            work_authorization IN (
                'no_restriction_mentioned',
                'local_authorization_required',
                'specific_authorization_required',
                'unknown'
            )
        ),

    visa_sponsorship TEXT NOT NULL
        CHECK (
            visa_sponsorship IN (
                'available',
                'not_available',
                'not_mentioned',
                'unknown'
            )
        ),

    -- Score breakdown
    skills_score INTEGER NOT NULL
        CHECK (skills_score BETWEEN 0 AND 30),

    experience_score INTEGER NOT NULL
        CHECK (experience_score BETWEEN 0 AND 25),

    role_alignment_score INTEGER NOT NULL
        CHECK (role_alignment_score BETWEEN 0 AND 15),

    location_score INTEGER NOT NULL
        CHECK (location_score BETWEEN 0 AND 15),

    growth_potential_score INTEGER NOT NULL
        CHECK (growth_potential_score BETWEEN 0 AND 15),

    -- Lets you invalidate old cached evaluations when
    -- you change your prompt or candidate profile
    prompt_version INTEGER NOT NULL DEFAULT 1,
    candidate_profile_version INTEGER NOT NULL DEFAULT 1,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (description_id)
        REFERENCES descriptions(id)
);


CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,
    company TEXT,

    url TEXT NOT NULL UNIQUE,

    source TEXT,
    source_job_id TEXT,

    location TEXT,

    -- What JobSpy/source says, separate from AI classification.
    source_is_remote INTEGER
        CHECK (
            source_is_remote IS NULL
            OR source_is_remote IN (0, 1)
        ),

    description_id INTEGER NOT NULL,
    evaluation_id INTEGER,

    why_skipped TEXT,

    first_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (description_id)
        REFERENCES descriptions(id),

    FOREIGN KEY (evaluation_id)
        REFERENCES evaluations(id)
);


CREATE INDEX IF NOT EXISTS idx_jobs_description_id
ON jobs(description_id);

CREATE INDEX IF NOT EXISTS idx_jobs_evaluation_id
ON jobs(evaluation_id);

CREATE INDEX IF NOT EXISTS idx_evaluations_percentage
ON evaluations(percentage);

CREATE INDEX IF NOT EXISTS idx_evaluations_seniority
ON evaluations(seniority);

CREATE INDEX IF NOT EXISTS idx_evaluations_work_arrangement
ON evaluations(work_arrangement);

CREATE INDEX IF NOT EXISTS idx_evaluations_remote_scope
ON evaluations(remote_scope);
"""

JSON_FIELDS = (
    "allowed_locations",
    "role_families",
    "matched_skills",
    "missing_required_skills",
    "missing_preferred_skills",
    "hard_blockers",
)
SCORE_FIELDS = (
    "skills",
    "experience",
    "role_alignment",
    "location",
    "growth_potential",
)


@contextmanager
def connect():
    conn = sqlite3.connect(data_path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def initialize_database():
    with connect() as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("BEGIN IMMEDIATE")
        for statement in SCHEMA.split(";"):
            if statement.strip():
                conn.execute(statement)


def _nullable(value):
    """Convert missing pandas values and numpy scalars to SQLite-safe values."""
    if value is None or pd.isna(value):
        return None
    return value.item() if hasattr(value, "item") else value


def get_evaluation_hash(job, cv):
    """Key the cache by job context, profile contents, and evaluation versions."""
    context = {
        "title": _nullable(job["title"]),
        "description_hash": hash_text(job["description"]),
        "location": _nullable(job.get("location")),
        "country": _nullable(job.get("country")),
        "source_is_remote": _nullable(job.get("is_remote")),
        "prompt_version": PROMPT_VERSION,
        "candidate_profile_version": CANDIDATE_PROFILE_VERSION,
        "candidate_profile_hash": hash_text(cv),
    }
    if context["source_is_remote"] is not None:
        context["source_is_remote"] = int(context["source_is_remote"])
    return hash_text(json.dumps(context, sort_keys=True, ensure_ascii=False))


def _insert_description(conn, description):
    description_hash = hash_text(description)
    conn.execute(
        """INSERT INTO descriptions (description_hash, description)
           VALUES (?, ?) ON CONFLICT(description_hash) DO NOTHING""",
        (description_hash, description),
    )
    return conn.execute(
        "SELECT id FROM descriptions WHERE description_hash = ?",
        (description_hash,),
    ).fetchone()["id"]


def insert_description(description):
    with connect() as conn:
        return _insert_description(conn, description)


def _insert_job(conn, job, why_skipped, evaluation_id):
    description_id = _insert_description(conn, job["description"])
    if evaluation_id is not None:
        evaluation = conn.execute(
            "SELECT description_id FROM evaluations WHERE id = ?", (evaluation_id,)
        ).fetchone()
        if evaluation is None or evaluation["description_id"] != description_id:
            raise ValueError("Evaluation does not belong to the job description")
    source_is_remote = _nullable(job.get("is_remote"))
    values = (
        job["title"],
        _nullable(job.get("company")),
        job["job_url"],
        _nullable(job.get("site")),
        _nullable(job.get("id")),
        _nullable(job.get("location")),
        int(source_is_remote) if source_is_remote is not None else None,
        description_id,
        evaluation_id,
        why_skipped,
    )
    return conn.execute(
        """INSERT INTO jobs (
            title, company, url, source, source_job_id, location,
            source_is_remote, description_id, evaluation_id, why_skipped
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            title = excluded.title,
            company = excluded.company,
            source = excluded.source,
            source_job_id = excluded.source_job_id,
            location = excluded.location,
            source_is_remote = excluded.source_is_remote,
            description_id = excluded.description_id,
            evaluation_id = excluded.evaluation_id,
            why_skipped = excluded.why_skipped,
            last_seen_at = CURRENT_TIMESTAMP
        RETURNING id""",
        values,
    ).fetchone()["id"]


def insert_job(job, why_skipped=None, evaluation_id=None):
    with connect() as conn:
        return _insert_job(conn, job, why_skipped, evaluation_id)


def bulk_insert(df, why_skipped):
    if df.empty:
        return
    with connect() as conn:
        for job in df.to_dict(orient="records"):
            _insert_job(conn, job, why_skipped, None)


def insert_evaluation(evaluation_hash, description_id, evaluation):
    scores = evaluation["score_breakdown"]
    if sum(scores[field] for field in SCORE_FIELDS) != evaluation["percentage"]:
        raise ValueError("Percentage must equal the score breakdown total")
    for field in JSON_FIELDS:
        if not isinstance(evaluation[field], list) or not all(
            isinstance(item, str) for item in evaluation[field]
        ):
            raise ValueError(f"{field} must be an array of strings")
    fields = [
        "evaluation_hash",
        "description_id",
        "why_good_fit",
        "what_missing",
        "percentage",
        "work_arrangement",
        "remote_scope",
        "seniority",
        *JSON_FIELDS,
        "minimum_experience_years",
        "student_status_required",
        "work_authorization",
        "visa_sponsorship",
        *(f"{field}_score" for field in SCORE_FIELDS),
        "prompt_version",
        "candidate_profile_version",
    ]
    values = (
        evaluation_hash,
        description_id,
        evaluation["why_good_fit"],
        evaluation["what_is_missing"],
        evaluation["percentage"],
        evaluation["work_arrangement"],
        evaluation["remote_scope"],
        evaluation["seniority"],
        *(json.dumps(evaluation[field], ensure_ascii=False) for field in JSON_FIELDS),
        evaluation["minimum_experience_years"],
        evaluation["student_status_required"],
        evaluation["work_authorization"],
        evaluation["visa_sponsorship"],
        *(scores[field] for field in SCORE_FIELDS),
        PROMPT_VERSION,
        CANDIDATE_PROFILE_VERSION,
    )
    with connect() as conn:
        conn.execute(
            f"INSERT INTO evaluations ({', '.join(fields)}) "
            f"VALUES ({', '.join('?' for _ in fields)}) "
            "ON CONFLICT(evaluation_hash) DO NOTHING",
            values,
        )
        return conn.execute(
            "SELECT id FROM evaluations WHERE evaluation_hash = ?", (evaluation_hash,)
        ).fetchone()["id"]


def get_info_from_hash(evaluation_hash):
    """Return the complete cached evaluation using the AI response field names."""
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM evaluations WHERE evaluation_hash = ?", (evaluation_hash,)
        ).fetchone()
    if row is None:
        return None
    result = dict(row)
    result["what_is_missing"] = result.pop("what_missing")
    for field in JSON_FIELDS:
        result[field] = json.loads(result[field])
    result["score_breakdown"] = {
        field: result.pop(f"{field}_score") for field in SCORE_FIELDS
    }
    return result


initialize_database()
