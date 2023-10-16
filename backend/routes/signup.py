import secrets
from datetime import datetime, timedelta
from routes import frontend
from flask_cors import cross_origin
from flask_login import current_user
from forms import SignupForm
from models.user import User
from flask import jsonify, request
# from config import bcrypt

def send_verification_email(user):
    verification_code = secrets.token_hex(16)
    user.verification_code = verification_code
    user.verification_expires_at = datetime.utcnow() + timedelta(minutes=30)
    user.save()


@frontend.route('/signup', methods=['POST'])
@cross_origin(allow_headers=['Content-Type', 'X-CSRFToken'], allow_methods=['POST'])
# @csrf.exempt
def signup():
    if current_user.is_authenticated:
        return ('/')
    form = SignupForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            password=form.password.data,
            verified=False,
            verification_code='12233'
        )
        user.save()
        return jsonify({'message': 'Registration successful'})

    # Handle form validation errors
    return jsonify({'error': 'Registration failed', 'errors': form.errors}), 400
