# forms/payment.py
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, StringField
from wtforms.validators import InputRequired, NumberRange, Email, DataRequired


class AuthPaymentForm(FlaskForm):
    amount = DecimalField('Amount', validators=[
        InputRequired(message='Amount is required'),
        NumberRange(min=1, message='Amount must be at least 1')
    ], render_kw={'placeholder': 'Amount'})
    submit = SubmitField('Make Payment', render_kw={'style': "background-color: rgb(240, 60, 2);"})


class PaymentForm(FlaskForm):
    amount = DecimalField('Amount', validators=[
        InputRequired(message='Amount is required'),
        NumberRange(min=1, message='Amount must be at least 1')
    ], render_kw={'placeholder': 'Amount'})
    email = StringField('Email', validators=[Email(), DataRequired()], render_kw={'placeholder': 'Email'})
    submit = SubmitField('Make Payment', render_kw={'style': "background-color: rgb(240, 60, 2);"})
