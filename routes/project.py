#!/usr/bin/env python3

"""
Handles All related project stuffs
"""
import os
import secrets

from config import db, app
from forms.project import ProjectForm
from routes import frontend
from models.project import Project
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from PIL import Image


def save_picture_project(project_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(project_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, 'templates/static/img/project_pics', picture_filename)
    print("Picture Filename:", picture_filename)
    print("Picture Path:", picture_path)

    output_size = (960, 540)
    i = Image.open(project_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename


@frontend.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        if form.category.data == '':
            form.category.data = 'Miscellaneous'
        if form.picture.data:
            picture_filename = save_picture_project(form.picture.data)
        else:
            picture_filename = None
        project = Project(campaign_name=form.campaign_name.data,
                          description=form.description.data,
                          target_amount=form.target_amount.data,
                          end_date=form.deadline.data,
                          category=form.category.data,
                          project_picture=picture_filename,
                          user=current_user)
        project.save()
        flash('Project created successfully', 'success')
        # return render_template('create_project.html', form=form)
        return redirect(url_for('frontend.create_project'))
    return render_template('create_project.html', form=form)


@frontend.route('/user_project', methods=['GET'])
@login_required
def user_project():
    user_projects = Project.query.order_by(Project.created_at.desc()).filter_by(user=current_user).all()
    return render_template('dashboard.html', user_projects=user_projects)


@frontend.route('/project')
def project():
    return render_template('campaign-list.html')
