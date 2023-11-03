#!/usr/bin/env python3


from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
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
    project_id = StringField('Project Id', validators=[DataRequired()])
    request_payment = SubmitField('Request Payment')
    
    def verify_withdrawal_amount(self, amount):
        """
        Verify withdrawal amount
        """
        try:
            project = Project.find_obj_by(id=self.project_id.data)
            if self.amount.data > project.current_amount:
                raise ValidationError("The withdrawal amount exceeds the current project balance")
            return "Amount verified"
        except NoResultFound:
            raise ValidationError("The project does not exist")
    
    def validate_project_id(self, project_id):
        """Verify project id"""
        try:
            query = Project.find_obj_by(id=self.project_id)
        except IntegrityError:
            raise ValidationError("Project not found")
