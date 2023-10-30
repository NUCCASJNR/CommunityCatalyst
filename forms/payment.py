# forms/payment.py
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, StringField
from wtforms.validators import InputRequired, NumberRange, Email, DataRequired

class PaymentForm(FlaskForm):
    amount = DecimalField('Amount', validators=[
        InputRequired(message='Amount is required'),
        NumberRange(min=1, message='Amount must be at least 1')
    ])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Make Payment')
