#!/usr/bin/env python3
""" module serves as a central place to store common functions used in
different parts of The Flask application. These functions are shared and
imported by other modules, such as routes/signup.py and routes/verify.py,
to avoid circular import issues and promote code reusability."""

from flask import render_template, url_for
import secrets
from datetime import datetime, timedelta
import requests
from os import getenv
from routes import frontend


def send_verification_email(user):
    """
    Sends a verification email to a user with a verification code
    and a link to verify their account.
    """

    verification_code = secrets.token_hex(16)
    user.verification_code = verification_code
    user.verification_expires_at = datetime.utcnow() + timedelta(minutes=30)
    user.save()

    verification_url = url_for('verify', verification_code=verification_code, _external=True, _scheme='https')
    html_body = render_template('verification.html', username=user.username, verification_url=verification_url)
    API_KEY = getenv("ELASTIC_EMAIL")
    sender = 'community-catalyst@codewithalareef.tech'
    receiver = user.email
    subject = 'Account Verification'
    url = 'https://api.elasticqemail.com/v2/email/send'

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


@frontend.route('/')
def home():
    return render_template('index.html')
