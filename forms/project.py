#!/usr/bin/env python3


from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, DecimalField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ProjectForm(FlaskForm):
    """
    Project Form class
    """
    campaign_name = StringField('Campaign Name', validators=[DataRequired(), Length(max=126)])
    description = TextAreaField('Description', validators=[DataRequired()])
    target_amount = DecimalField('Goal Amount', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    deadline = DateField('End Date', format='%Y-%m-%d')
    picture = FileField('Project Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    category = StringField('Category', validators=[DataRequired(), Length(max=126)])
    # location = StringField('Location', validators=[Length(max=126)])
    submit = SubmitField('Submit')
