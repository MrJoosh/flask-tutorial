import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

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
    # Email error alerting
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
    # Logging to file
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        filename='logs/microblog.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    )
    file_handler.setLevel(logging.INFO)
    webapp.logger.addHandler(file_handler)  # pylint: disable=no-member

    webapp.logger.setLevel(logging.INFO)  # pylint: disable=no-member
    webapp.logger.info('Microblog Startup')  # pylint: disable=no-member
