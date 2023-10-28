from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, DateField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class ProfileForm(FlaskForm):
    """Profile Form Class"""
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=126)])
    middle_name = StringField('Middle Name', validators=[Length(max=126)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=126)])
    picture = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'])], render_kw={'style': 'display: none;'})
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    contact = StringField('Contact', validators=[Length(max=15)])
    email = StringField('Email', validators=[Email(), DataRequired()])
    address = StringField('Address', validators=[Length(max=126)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)],
                           render_kw={'placeholder': 'johndoe123'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)],
                             render_kw={'placeholder': "Must be at least 8 characters"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={'placeholder': 'Confirm Password'})
    submit = SubmitField('Update')
