from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from . import login_manager
from sharedmodels.models import User

'''
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    # Relationship
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    api_keys = db.relationship('APIKey', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class APIKey(db.Model):
    __tablename__ = 'apikey'
    id = db.Column(db.Integer, primary_key=True)
    application = db.Column(db.String(64))
    apikey = db.Column(db.String(64), unique=True)
    # Relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
'''

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
