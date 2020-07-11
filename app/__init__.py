import logging
from logging.handlers import SMTPHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config

webapp = Flask(__name__)
webapp.config.from_object(Config)
db = SQLAlchemy(webapp)
migrate = Migrate(webapp, db)
login = LoginManager(webapp)
login.login_view = 'login'

from app import routes, models, errors

if not webapp.debug:
    if webapp.config['MAIL_SERVER']:
        auth = None
        if webapp.config['MAIL_USERNAME'] or webapp.config['MAIL_PASSWORD']:
            auth = (webapp.config['MAIl_USERNAME'], webapp.config['MAIL_PASSWORD'])
        secure = None
        if webapp.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(webapp.config['MAIL_SERVER'], webapp.config['MAIL_PORT']),
            fromaddr='no-reply@{}'.format(webapp.config['MAIL_SERVER']),
            toaddrs=webapp.config['ADMINS'],
            subject='Microblog Failure',
            credentials=auth,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        webapp.logger.addHandler(mail_handler)  # pylint: disable=no-member
