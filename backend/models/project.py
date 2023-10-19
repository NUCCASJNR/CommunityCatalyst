#!/usr/bin/env python3

"""
Project's Table
"""

from models.base_model import BaseModel, db, datetime
from models.user import User


class Project(BaseModel):
    """
    Project Class
    Args:
    """
    __tablename__ = 'projects'
    user_id = \
        db.Column(db.String(126), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(126), nullable=False)
    description = db.Column(db.Text, nullable=False)
    goal_amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    current_amount = \
        db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    project_picture = db.Column(db.String(126), nullable=True)
    end_date = db.Column(db.DateTime)
    category = db.Column(db.String(126))
    location = db.Column(db.String(126))

    def __init__(self, *args, **kwargs):
        """
        Initialization method
        """
        super().__init__(*args, **kwargs)
        self.start_date = datetime.now()
