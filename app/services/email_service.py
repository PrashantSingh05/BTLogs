import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def send_reset_email(to_email, reset_link):
    sender = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")

    subject = "Reset Your Password - BTLogs"

    body = f"""
Hello,

Click the link below to reset your password:

{reset_link}

If you did not request this, ignore this email.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())
        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email failed:", e)