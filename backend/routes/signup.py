from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import current_user
from forms.signup import SignupForm
from models.user import User, db
from routes import frontend
from routes.common import send_verification_email
from wtforms import ValidationError


@frontend.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Signup route
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        try:
            form.validate_username(form.username)
            form.validate_email(form.email)
        except ValidationError as e:
            flash(str(e), 'danger')
            return render_template('index.html', form=form)
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
        return jsonify({"success": "user created"})
    return render_template('index.html', form=form)

