#!/usr/bin/env python3


from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from sqlalchemy.exc import IntegrityError
from models.project import Project


class WithdrawalForm(FlaskForm):
    """
    Withdrawal form that inherits from flask form
    """
    campaign_name = StringField('Campaign Name', validators=[DataRequired(), Length(max=126)])
    acc_name = StringField('Account Name', validators=[DataRequired(), Length(max=126)])
    acc_number = StringField('Account Number', validators=[DataRequired(), Length(max=126)])
    bank = StringField('Bank', validators=[DataRequired(), Length(max=126)])
    amount = DecimalField('Amount', validators=[DataRequired()])
    project_id = StringField('Project_id', validators=[DataRequired()])
    request_payment = SubmitField('Request Payment')
    
    def verify_withdrawal_amount(self, amount):
        """
        Verify withdrawal amount
        """
        funds_contributed = {"id": self.project_id}
        query = Project.find_obj_by(**funds_contributed)
        if query:
            if self.amount.data > query.current_amount:
                return f"You cannot withdraw more than {query.current_amount}"
            else:
                return "Amount verified"
        else:
            raise ValidationError("Project not found")
    
    def validate_project_id(self, project_id):
        """Verify project id"""
        try:
            query = Project.find_obj_by(id=project_id)
        except IntegrityError:
            raise ValidationError("Project not found")
