from threading import Thread

from flask import render_template, current_app
from flask_mail import Message
from flask_babel import gettext as _

from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=recipients,
        body=text_body,
        html=html_body
    )
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
