from app import webapp, db
from app.models import User, Post

@webapp.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
