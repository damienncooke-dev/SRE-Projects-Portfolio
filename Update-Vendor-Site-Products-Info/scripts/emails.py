#!/usr/bin/env python3

"""
Module to define the methods to create and send emails.  This script uses the 'dotenv' package to load the email credentials, basic mail attributes, and SMTP server information
Called by report_email.py

"""

import smtplib
import mimetypes
import email.message
import os
from dotenv import load_dotenv
from pathlib import Path


def generate_email(subject, body, attachments):
    main_dir = Path(__file__).parent.parent
    env_path = main_dir / ".dotenv"
    load_dotenv(dotenv_path=env_path)

    # Basic email setup
    msg = email.message.EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("EMAIL_SENDER")
    msg['To'] = os.getenv("EMAIL_RECIPIENT")
    msg.set_content(body)

    # Attachments
    mime_type, _ = mimetypes.guess_type(attachments)
    mime_type, mime_subtype = mime_type.split("/", 1)
    with open(attachments, "rb") as attach:
        msg.add_attachment(attach.read(), maintype=mime_type, subtype=mime_subtype, filename=attachments)
    return msg

def send_email(message):
    main_dir = Path(__file__).parent.parent
    env_path = main_dir / ".dotenv"
    load_dotenv(dotenv_path=env_path)
    print(message)
    # SMTP server setup
    email_server = os.getenv("EMAIL_SERVER")
    email_port = os.getenv("EMAIL_PORT")
    email_sender = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("ICLOUD_APP_PASSWORD")
    with smtplib.SMTP(email_server, int(email_port)) as server:
       server.starttls()
       server.login(email_sender, email_password)
       server.send_message(message)
       server.quit()


