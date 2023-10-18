from flask import render_template, redirect, url_for
from flask_login import current_user
from forms import SignupForm
from models.user import User
from routes import frontend
from routes.common import send_verification_email


# @frontend.route('/')
# def home():
#     return render_template('index.html')


@frontend.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = User.hash_password(form.password.data)
        user = User(
            first_name=form.firstName.data,
            last_name=form.lastName.data,
            username=form.username.data,
            password=hashed_password,
            verified=False
        )
        user.save()
        send_verification_email(user)
    return render_template('signup.html')