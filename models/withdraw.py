#!/usr/bin/env python3

from models.base_model import BaseModel, db
from models.contribution import Contribution

class WithDraw(BaseModel):
    """Withdrawal class for handling funds withdrawal"""
    __tablename__ = 'withdrawals'
    amount = db.Column(db.Numeric(precision=10, scale=2))
    project_id = db.Column(db.String(126), db.ForeignKey('projects.id'), nullable=False)
    user = db.relationship('User', back_populates='withdrawals')
