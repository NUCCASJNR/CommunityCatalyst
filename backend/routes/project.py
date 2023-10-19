#!/usr/bin/env python3

"""
Handles All related project stuffs
"""

from forms.project import ProjectForm
from frontend import route
from routes.common import upload_image
from models.project import Project
from flask import flash

@frontend.route('/create-project', methods=['GET', 'POST'])
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project_image = form.project_picture.data
        if project_image:
            file_path = upload_image()
        file_path = ''
        project = Project(
            title=form.title.data,
            description=form.description.data,
            goal_amount=form.goal_amount.data,
            current_amount=form.current_amount.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            profile_picture=file_path,
            category=form.category.data,
            location=form.location.data
        )
        project.save()
        flash('Project created successfully', 'success')
        