#!/usr/bin/env python3

"""
Comments Table
"""
from models.base_model import BaseModel, db
from models.project import User, Project


class Comment(BaseModel, db.Model):
    """Comment class"""
    __tablename__ = 'comments'
    user_id = \
        db.Column(db.String(126), db.ForeignKey('users.id'), nullable=False)
    project_id = \
        db.Column(db.String(126), db.ForeignKey('projects.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
