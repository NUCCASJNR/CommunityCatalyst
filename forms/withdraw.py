#!/usr/bin/env python3


from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length


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
    request_payment = SubmitField('Reqeust Payment')