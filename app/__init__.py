import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from elasticsearch import Elasticsearch
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please login to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    webapp = Flask(__name__)
    webapp.config.from_object(config_class)

    db.init_app(webapp)
    migrate.init_app(webapp, db)
    login.init_app(webapp)
    mail.init_app(webapp)
    bootstrap.init_app(webapp)
    moment.init_app(webapp)
    babel.init_app(webapp)

    # Register main blueprint
    from app.main import bp as main_bp
    webapp.register_blueprint(main_bp)

    # Register error handling blueprint
    from app.errors import bp as errors_bp
    webapp.register_blueprint(errors_bp)

    # Register authentication blueprint
    from app.auth import bp as auth_bp
    webapp.register_blueprint(auth_bp, url_prefix='/auth')

    # Register elasticsearch instance if configured
    webapp.elasticsearch = Elasticsearch([webapp.config['ELASTICSEARCH_URL']]) \
                            if webapp.config['ELASTICSEARCH_URL'] else None

    if not webapp.debug and not webapp.testing:
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

    return webapp


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
