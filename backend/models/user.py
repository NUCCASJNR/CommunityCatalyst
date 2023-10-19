#!/usr/bin/env python3

"""
Users table
"""
from models.base_model import BaseModel, db
from uuid import uuid4
import bcrypt

def generate_verification_code() -> str:
    """
    Generates Auth token
    :return:
    """
    token = str(uuid4())
    return token


class User(BaseModel):
    """
    User's Table
    Args:
        username: username of the user
        email: email of the user
        password: password of the user
        first_name: Firstname of the user
        last_name: Lastname of the user
        profile_picture: profilePicture of user
        verification_code: user's verification code
         verified:
    """
    __tablename__ = 'users'
    username = db.Column(db.String(126), nullable=False, unique=True)
    email = db.Column(db.String(126), nullable=False, unique=True)
    password = db.Column(db.String(126), nullable=False)
    first_name = db.Column(db.String(126), nullable=False)
    last_name = db.Column(db.String(126), nullable=False)
    profile_picture = db.Column(db.String(126), nullable=True)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    verification_code = db.Column(db.String(60))
    verification_expires_at = db.Column(db.DateTime, nullable=True)
    projects = db.relationship('Project', backref='user')
    contributions = db.relationship('Contribution', backref='user', lazy=True)
    
    @staticmethod
    def hash_password(password):
        pwd_byte = bytes(password, encoding='utf-8')
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(pwd_byte, salt)
        return hashed_pwd
    
    @staticmethod
    def check_password_hash(password_to_check, password_hash):
        pwd_byte = bytes(password_to_check, encoding='utf-8')
        return bcrypt.checkpw(pwd_byte, password_hash)