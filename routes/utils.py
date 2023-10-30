#!/usr/bin/env python3
""" module serves as a central place to store common functions used in
different parts of The Flask application. These functions are shared and
imported by other modules, such as routes/signup.py and routes/verify.py,
to avoid circular import issues and promote code reusability."""
from PIL import Image
from flask import render_template, url_for, request, flash, redirect
import secrets
from datetime import datetime, timedelta
import requests
from os import getenv
from flask_login import current_user, login_user
from config import app
from routes import frontend
from werkzeug.utils import secure_filename
import os
from models.project import Project
from models.user import User, db


def send_verification_email(user):
    """
    Sends a verification email to a user with a verification code
    and a link to verify their account.
    """

    verification_code = secrets.token_hex(16)
    user.verification_code = verification_code
    user.verification_expires_at = datetime.utcnow() + timedelta(minutes=30)
    user.save()

    verification_url = url_for('frontend.verify', verification_code=verification_code, _external=True, _scheme='https')
    html_body = render_template('verification.html', username=user.username, verification_url=verification_url)
    API_KEY = getenv("ELASTIC_EMAIL")
    sender = 'community-catalyst@polyglotte.tech'
    receiver = user.email
    subject = 'Account Verification'
    url = 'https://api.elasticemail.com/v2/email/send'

    request_payload = {
        'apikey': API_KEY,
        'from': sender,
        'to': receiver,
        'subject': subject,
        'bodyHtml': html_body,
        'isTransactional': False
    }
    response = requests.post(url, data=request_payload)
    if response.status_code == 200:
        print('Email successfully sent to user')
    print(f'Error occurred with error code: {response.status_code}')


def save_picture(project_picture, path):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(project_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, f'static/img/{path}', picture_filename)
    print("Picture Filename:", picture_filename)
    print("Picture Path:", picture_path)

    output_size = (960, 540)
    i = Image.open(project_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename


def upload_image():
    """
    Handles image uploading
    """
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No file selected'
    if file:
        filename = secure_filename(file.filename)
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
        if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            upload_folder = '/tmp/community_catalyst'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            return file_path
        else:
            return 'Invalid file extension'


@frontend.route('/')
def home():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('index.html', projects=projects)


@frontend.route('/verify/<string:verification_code>', methods=['GET', 'POST'])
def verify(verification_code):
    """
    Verification route
    Verifies a user based on the verification code provided
    """
    if current_user.is_authenticated:
        return redirect(url_for('frontend.home'))
    query = {'verification_code': verification_code}
    user = User.find_obj_by(**query)
    if user:
        if user.verification_expires_at and datetime.utcnow() > user.verification_expires_at:
            user.delete()
            flash('The verification link has expired,'
                  ' Please signup again to receive a new verification code',
                  'danger')
            return redirect(url_for('frontend.home'))
        user.verified = True
        user.verification_code = None
        User.save(user)
        login_user(user)
        flash('Your account has successfully been created'
              ' and you have been logged in, Happy Funding', 'success')
    else:
        flash('Invalid verification code. Please try again', 'danger')
    return redirect(url_for('frontend.home'))


@frontend.route('/about')
def about():
    return render_template('about.html')


@frontend.route('/contact')
def contact():
    return render_template('contact.html')
