#!/usr/bin/env python3

from models.base_model import BaseModel, db
from models.contribution import Contribution

class WithDraw(BaseModel):
    """Withdrawal class for handling funds withdrawal"""
    __tablename__ = 'withdrawals'
    acc_name = db.Column(db.Text, nullable=False)
    acc_number = db.Column(db.BIGINT, nullable=False)
    bank = db.Column(db.String(126), nullable=False)
    user_id = \
        db.Column(db.String(126), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2))
    campaign_name = db.Column(db.String(126), nullable=False)
    project_id = db.Column(db.String(126), db.ForeignKey('projects.id'), nullable=False)
    status = db.Column(db.String(126), nullable=False)
    user = db.relationship('User', back_populates='withdrawals')
