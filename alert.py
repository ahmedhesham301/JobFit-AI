import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from html import escape
from urllib.parse import urlsplit

from pandas import isna


def _display(value, default="Not specified"):
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value) if value else default
    if value is None or isna(value):
        return default
    return str(value).strip() or default


def _label(value):
    return _display(value).replace("_", " ").capitalize()


def _job_details(job):
    """Use the same details in the HTML and plain-text email."""
    rows = [
        ("Location", _display(job.get("location"))),
        ("Work arrangement", _label(job.get("work_arrangement"))),
        ("Remote scope", _label(job.get("remote_scope"))),
        ("Allowed locations", _display(job.get("allowed_locations"))),
        ("Seniority", _label(job.get("seniority"))),
    ]
    experience = job.get("minimum_experience_years")
    rows.append(("Minimum experience (years)", _display(experience)))
    rows.extend(
        [
            (
                "Why you're a good fit",
                _display(job.get("why_good_fit", job.get("why I'm I a good fit"))),
            ),
            (
                "Main gaps",
                _display(job.get("what_is_missing", job.get("what I'm I missing"))),
            ),
            ("Matched skills", _display(job.get("matched_skills"), "None identified")),
            (
                "Missing required skills",
                _display(job.get("missing_required_skills"), "None identified"),
            ),
            (
                "Missing preferred skills",
                _display(job.get("missing_preferred_skills"), "None identified"),
            ),
            ("Hard blockers", _display(job.get("hard_blockers"), "None identified")),
            ("Student status required", _label(job.get("student_status_required"))),
            ("Work authorization", _label(job.get("work_authorization"))),
            ("Visa sponsorship", _label(job.get("visa_sponsorship"))),
        ]
    )
    scores = job.get("score_breakdown")
    if scores:
        limits = {
            "skills": 30,
            "experience": 25,
            "role_alignment": 15,
            "location": 15,
            "growth_potential": 15,
        }
        rows.append(
            (
                "Score breakdown",
                " · ".join(
                    f"{_label(key)}: {scores[key]}/{limit}"
                    for key, limit in limits.items()
                    if key in scores
                ),
            )
        )
    return rows


def send_email(sender, receiver, password, good_fit_jobs, summary=None):
    print("preparing message")
    count = len(good_fit_jobs)
    noun = "job" if count == 1 else "jobs"
    intro = f"{count} matching {noun}, ranked by fit score."
    text_parts = ["My Job Alert", intro]
    html_parts = [
        '<html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #2c3e50;">',
        f"<h1>My Job Alert</h1><p>{intro}</p>",
    ]

    for job in sorted(good_fit_jobs, key=lambda job: job["percentage"], reverse=True):
        title = _display(job.get("title"), "Untitled job")
        heading = f'{title} — {job["percentage"]}% match'
        rows = _job_details(job)
        text_parts.append("\n" + heading)
        html_parts.append(
            f'<section style="margin-bottom: 28px;"><h2>{escape(heading)}</h2>'
        )
        for label, value in rows:
            text_parts.append(f"{label}: {value}")
            style = (
                ' style="color: #a12622; font-weight: bold;"'
                if label == "Hard blockers" and value != "None identified"
                else ""
            )
            html_parts.append(f"<p{style}><b>{escape(label)}:</b> {escape(value)}</p>")

        url = _display(job.get("url", job.get("job_url")), "")
        try:
            parsed = urlsplit(url)
            valid_url = parsed.scheme in ("https", "http") and bool(parsed.netloc)
        except ValueError:
            valid_url = False
        if valid_url:
            text_parts.append(f"View job / apply: {url}")
            html_parts.append(
                f'<p><a href="{escape(url, quote=True)}">View job / apply</a></p>'
            )
        else:
            text_parts.append("Job link unavailable")
            html_parts.append("<p>Job link unavailable</p>")
        html_parts.append("</section>")

    if summary:
        text_parts.append("\n" + summary)
        html_parts.append(
            f'<pre style="white-space: pre-wrap;">{escape(summary)}</pre>'
        )
    html_parts.append("</body></html>")

    message = MIMEMultipart("alternative")
    message.attach(MIMEText("\n".join(text_parts), "plain", "utf-8"))
    message.attach(MIMEText("\n".join(html_parts), "html", "utf-8"))
    message["Subject"] = f"MY JOB ALERT: {count} matching {noun}"
    message["From"] = sender
    message["To"] = receiver

    print(f"Sending email with {count} jobs")
    with smtplib.SMTP("smtp.gmail.com", timeout=60, port=587) as connection:
        connection.starttls()
        connection.login(user=sender, password=password)
        connection.sendmail(
            from_addr=sender,
            to_addrs=receiver,
            msg=message.as_string(),
        )
