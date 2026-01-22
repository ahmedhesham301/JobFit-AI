import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender, receiver, password, good_fit_jobs):
    print("preparing message")
    html_body = """<html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color: #2c3e50;">My Job Alert</h2>
        <p><b>{count} jobs</b> have been found that match your profile:</p>
        <ul style="padding-left: 20px;">
    """.format(
        count=len(good_fit_jobs)
    )

    for job in good_fit_jobs:
        html_body += f"""
        <li style="margin-bottom: 15px;">
            <p><b>Title:</b> {job[1]}</p>
            <p><b>URL:</b> <a href="{job[0]}">{job[0]}</a></p>
            <p><b>Percentage:</b> {job[3]}</p>

        </li>
        """

    html_body += """
        </ul>
    </body>
    </html>
    """

    message = MIMEText(html_body, "html")
    message["Subject"] = f"MY JOB ALERT: {len(good_fit_jobs)} jobs has been found"
    message["From"] = sender
    message["To"] = receiver

    print(f"Sending email with {len(good_fit_jobs)} jobs")
    with smtplib.SMTP("smtp.gmail.com", timeout=60, port=587) as connection:
        connection.starttls()
        connection.login(user=sender, password=password)
        connection.sendmail(
            from_addr=sender,
            to_addrs=receiver,
            msg=message.as_string(),
        )
        connection.close()
