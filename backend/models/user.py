#!/usr/bin/env python3

"""
Users table
"""
from models.base_model import BaseModel, db
from config import bcrypt
from uuid import uuid4


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
    verification_code = db.Column(db.String(126), nullable=False, unique=True)
    verified = db.Column(db.Integer, default=0)
