import secrets
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_cors import cross_origin
from flask_login import current_user
from forms import SignupForm
from models.user import User
from routes import frontend
from csrf_extension import csrf
from flask import current_app


def send_verification_email(user):
    verification_code = secrets.token_hex(16)
    user.verification_code = verification_code
    user.verification_expires_at = datetime.utcnow() + timedelta(minutes=30)
    user.save()


@frontend.route('/signup', methods=['POST'])
@cross_origin(allow_headers=['Content-Type', 'x-csrftoken'])
@csrf.exempt
def signup():
    current_app.logger.debug('Signup route called.')
    
    csrf_token = request.headers.get('x-csrftoken')
    current_app.logger.debug(f'CSRF Token from Header: {csrf_token}')
    if current_user.is_authenticated:
        return ('/')
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = User.hash_password(form.password.data)
        user = User(
            first_name=form.firstName.data,
            last_name=form.lastName.data,
            username=form.username.data,
            password=hashed_password,
            verified=False,
            verification_code='12233'
        )
        user.save()
        return jsonify({'message': 'Registration successful'})

    return jsonify({'error': 'Registration failed', 'errors': form.errors}), 400
