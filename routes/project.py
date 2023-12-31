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
from flask import flash, redirect, render_template, url_for, abort
from flask_login import login_required, current_user
from PIL import Image
from routes.utils import save_picture
from models.contribution import Contribution


@frontend.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        if form.category.data == '':
            form.category.data = 'Miscellaneous'
        if form.picture.data:
            picture_filename = save_picture(form.picture.data, 'project_pics')
        else:
            picture_filename = 'templates/static/img/project_pics/logo.png'
        project = Project(campaign_name=form.campaign_name.data,
                          description=form.description.data,
                          target_amount=form.target_amount.data,
                          start_date=form.start_date.data,
                          end_date=form.deadline.data,
                          category=form.category.data,
                          status='Active',
                          project_picture=picture_filename,
                          user=current_user)
        project.save()
        flash('Project created successfully', 'success')
        return redirect(url_for('frontend.create_project'))
    return render_template('create_project.html', form=form)


@frontend.route('/user_project', methods=['GET'])
@login_required
def user_project():
    user_projects = Project.query.order_by(Project.created_at.desc()).filter_by(user=current_user).all()
    return render_template('member_campaign-list.html', user_projects=user_projects)


@frontend.route('/project')
def project():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('campaign-list.html', projects=projects)


@frontend.route('/user_project/<project_id>/delete', methods=['GET', 'DELETE'])
@login_required
def delete_user_project(project_id):
    obj = {"id": project_id, "user": current_user}
    query = Project.find_obj_by(**obj)
    if query:
        query.delete()
        flash('Project successfully deleted', 'success')
        return redirect(url_for('frontend.dashboard'))
    abort(404)


@frontend.route('/user_gallery')
@login_required
def user_gallery():
    # Query pictures that belong to the current user
    pictures = Project.query.filter_by(user=current_user).order_by(Project.project_picture.desc()).all()
    return render_template('gallery.html', pictures=pictures)


@frontend.route('user_donation')
@login_required
def user_donation():
    query = {'user': current_user}
    donations = Contribution.query.filter_by(**query).all()
    project_ids = [donation.project_id for donation in donations]
    projects = Project.query.filter(Project.id.in_(project_ids)).all()
    # Combine donations and projects into a zipped list
    zipped_data = zip(donations, projects)

    return render_template('donation.html', zipped_data=zipped_data)