#!/usr/bin/env python3

"""Categories table"""
from models.base_model import BaseModel, db


class Category(BaseModel, db.Model):
    """Category class"""
    __tablename__ = 'categories'
    name = db.Column(db.String(126), nullable=False)
