#!/usr/bin/env python3

"""Contributions class"""

from models.base_model import BaseModel, db
from models.project import User, Project


class Contribution(BaseModel, db.Model):
    """
    contribution table
    """
    __tablename__ = 'contributions'
    user_id = \
        db.Column(db.String(126), db.ForeignKey('users.id'), nullable=False)
    project_id = \
        db.Column(db.String(126), db.ForeignKey('projects.id'), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2))
    user = db.relationship('User', back_populates='contributions')