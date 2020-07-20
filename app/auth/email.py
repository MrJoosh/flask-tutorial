from flask import render_template, current_app
from flask_babel import _
from app.email import send_email


def send_password_reset_email(user):
    token = user.get_password_reset_token()
    send_email(
        _('[Microblog] Reset your password'),
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
