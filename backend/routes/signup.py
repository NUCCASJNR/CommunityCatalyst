import secrets
from datetime import datetime, timedelta
from routes.app import app, bcrypt, db
from flask_login import current_user
from forms import SignupForm
from models.user import User


def send_verification_email(user):
    verification_code = secrets.token_hex(16)
    user.verification_code = verification_code
    user.verification_expires_at = datetime.utcnow() + timedelta(minutes=30)
    db.session.commit()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return ('/')
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            password=hashed_password,
            verified=False
        )
        User.save()
