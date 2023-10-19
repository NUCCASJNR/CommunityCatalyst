#!/usr/bin/env python3

"""Handles User Authentication and login"""

from flask import redirect, render_template, flash, url_for, request
from flask_login import login_user, current_user, login_required
from models.user import User
from forms.login import LoginForm
from routes import frontend
from routes.common import home
from models.project import Project


@frontend.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return redirect(url_for(home))
    form = LoginForm()

    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        password = form.password.data

        if '@' in username_or_email:
            user_query = {'email': username_or_email}
            user = User.find_obj_by(**user_query)

        else:
            user = User.find_obj_by(username=username_or_email)
        if user:
            if user.verified:
                hashed_password = User.hash_password(password)
                if user and user.check_password_hash(password, hashed_password):
                    login_user(user)
                    next_page = request.args.get('next')
                    flash('You have been logged in', 'success')
                    if next_page:
                        return redirect(next_page)
                    return redirect('dashboard')
                else:
                    flash('Login Unsuccessful. Please Check your username\
                        and password', 'danger')
            else:
                flash('You need to verify your account before you can log in'\
                    'danger')
        else:
            flash('Login Unsuccessful. Please Check your username\
                        and password', 'danger')
    return render_template('signin.html')


@frontend.route('/dashboard')
# @login_required
def dashboard():
    projects = Project.all()
    return render_template('dashboard.html', projects=projects)