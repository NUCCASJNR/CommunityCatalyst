#!/usr/bin/env python3

"""
Project's Table
"""

from models.base_model import BaseModel, db, datetime
from models.user import User
from decimal import Decimal

class Project(BaseModel, db.Model):
    """
    Project Class
    Args:
    """
    __tablename__ = 'projects'
    user_id = \
        db.Column(db.String(126), db.ForeignKey('users.id'), nullable=False)
    campaign_name = db.Column(db.String(126), nullable=False)
    description = db.Column(db.Text, nullable=False)
    target_amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    current_amount = \
        db.Column(db.Numeric(precision=10, scale=2), nullable=True, default=True)
    start_date = db.Column(db.DateTime, nullable=False)
    project_picture = db.Column(db.String(126), nullable=True)
    end_date = db.Column(db.DateTime)
    category = db.Column(db.String(126))
    contributions = db.relationship('Contribution', back_populates='project', cascade='all, delete-orphan')
    amount_left = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    status = db.Column(db.Enum('Active', 'Inactive', 'Completed'), default='Active')
    # location = db.Column(db.String(126))
    user = db.relationship('User', back_populates='projects', lazy=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.current_amount is None:
            self.current_amount = Decimal(0)
        self.amount_left = Decimal(self.target_amount - self.current_amount)

