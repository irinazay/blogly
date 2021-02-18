"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """Users"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    image_url = db.Column(db.Text)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Blog post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def formated_date(self):
        """Return formated date."""

        return self.created_at.strftime("%b %-d  %Y, %-I:%M %p")


def connect_db(app):
    """Connect database to Flask app."""

    db.app = app
    db.init_app(app)