from datetime import datetime

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=no-member
    username = db.Column(db.String(64), index=True, unique=True)  # pylint: disable=no-member
    email = db.Column(db.String(120), index=True, unique=True)  # pylint: disable=no-member
    password_hash = db.Column(db.String(128))  # pylint: disable=no-member
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # pylint: disable=no-member

    def __repr__(self):
        return "<User {}>".format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=no-member
    body = db.Column(db.String(140))  # pylint: disable=no-member
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # pylint: disable=no-member
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # pylint: disable=no-member

    def __repr__(self):
        return "<Post {}>".format(self.body)
