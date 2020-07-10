from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=no-member
    username = db.Column(db.String(64), index=True, unique=True)  # pylint: disable=no-member
    email = db.Column(db.String(120), index=True, unique=True)  # pylint: disable=no-member
    password_hash = db.Column(db.String(128))  # pylint: disable=no-member
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # pylint: disable=no-member

    def __repr__(self):
        return "<User {}>".format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=no-member
    body = db.Column(db.String(140))  # pylint: disable=no-member
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # pylint: disable=no-member
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # pylint: disable=no-member

    def __repr__(self):
        return "<Post {}>".format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))