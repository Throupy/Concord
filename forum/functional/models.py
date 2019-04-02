"""Database models."""
from datetime import datetime
from functional import db, login_manager
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    subscribed = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    banner_file = db.Column(db.String(20), nullable=False,
                            default='default_banner.jpg')

    def get_reset_token(self, expires_seconds=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "Post('%s', '%s')" % self.username, self.email


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # means we have a relationship with author

    def __repr__(self):
        return "Post('%s', '%s', '%s')" % self.title, self.date_posted, self.content
