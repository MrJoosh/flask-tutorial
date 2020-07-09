from flask import Flask
from config import Config

webapp = Flask(__name__)
webapp.config.from_object(Config)

from app import routes
