from threading import Thread

from flask import render_template
from flask_mail import Message

from app import webapp, mail


def send_async_email(webapp, msg):
    with webapp.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=recipients,
        body=text_body,
        html=html_body
    )
    Thread(target=send_async_email, args=(webapp, msg)).start()


def send_password_reset_email(user):
    token = user.get_password_reset_token()
    send_email(
        '[Microblog] Reset your password',
        sender='no-reply@microblog',
        recipients=[user.email],
        text_body=render_template(
            'email/reset_password.txt',
            user=user,
            token=token
        ),
        html_body=render_template(
            'email/reset_password.html',
            user=user,
            token=token,
        )
    )
