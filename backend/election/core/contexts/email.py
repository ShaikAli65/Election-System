import json
import smtplib
from email.message import EmailMessage

from election.core.constants import get_config


def send_email(recipient: str, subject: str, body: str):

    configs = get_config()
    with open(configs.gmail_path) as f:
        mail_creds = json.load(f)

    msg = EmailMessage()
    msg["From"] = mail_creds['email']
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    # Connect to the SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(mail_creds['email'],mail_creds['password'])
        smtp.send_message(msg)
