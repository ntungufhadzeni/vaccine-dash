import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(225), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, username, email, hashed_password, admin) -> None:
        self.username = username
        self.email = email
        self.encrypted_password = hashed_password
        self.is_admin = admin


    def __repr__(self):
        return f'User: {self.username}'
    

