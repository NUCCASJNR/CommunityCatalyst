#!/usr/bin/env python3


from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length


class ProjectForm(FlaskForm):
    """
    Project Form class
    """
    title = StringField('Title', validators=[DataRequired(), Length(max=126)])
    description = TextAreaField('Description', validators=[DataRequired()])
    goal_amount = DecimalField('Goal Amount', validators=[DataRequired()])
    current_amount = DecimalField('Current Amount', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')
    project_picture = FileField('Project Picture', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired(), Length(max=126)])
    location = StringField('Location', validators=[Length(max=126)])