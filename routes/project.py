#!/usr/bin/env python3

"""
Handles All related project stuffs
"""

from forms.project import ProjectForm
from routes import frontend
from routes.utils import upload_image
from models.project import Project
from flask import flash, redirect, render_template, url_for
from flask_login import login_required


@frontend.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project_image = form.project_picture.data
        if project_image:
            file_path = upload_image()
        else:
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
        return render_template('create_project.html', form=form)
    return render_template('create_project.html', form=form)


@frontend.route('/update_project/<user_id>/<id>', methods=['PUT'])
@login_required
def update_project(user_id, id):
    """
    Updates a project using the id provided
    """


@frontend.route('/project')
def project():
    return render_template('campaign-list.html')
