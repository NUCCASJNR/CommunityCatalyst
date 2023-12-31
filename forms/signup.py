#!/usr/bin/env python3

"""Forms Handler"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models.user import User


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'johndoe123@gmail.com'})
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)],
                           render_kw={'placeholder': 'johndoe123'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)],
                             render_kw={'placeholder': "Must be at least 8 characters"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],
                                    render_kw={'placeholder': 'Confirm Password'})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
               Validates user's username by checking if it exists
                in the users table before
               :param username: user's username
               :return:
                   Error if it exists
               """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username already exists')

    def validate_email(self, email):
        """
        Validates user's email by checking if it exists
         in the users table before
        :param email: user's email
        :return:
            Error if it exists
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already exists')
