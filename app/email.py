from flask_mail import Message

from app import mail


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=recipients,
        body=text_body,
        html=html_body
    )
    mail.send(msg)
