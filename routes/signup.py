from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import current_user
from forms.signup import SignupForm
from models.user import User
from routes import frontend
from routes.utils import send_verification_email
from wtforms import ValidationError
from routes.utils import home


@frontend.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Signup route
    """
    if current_user.is_authenticated:
        return redirect(url_for('frontend.dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        try:
            form.validate_username(form.username)
            form.validate_email(form.email)
        except ValidationError as e:
            flash(str(e), 'danger')
            return render_template('signup.html', form=form)
        hashed_password = User.hash_password(form.password.data)
        print(hashed_password)
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            password=hashed_password,
            email=form.email.data,
            verified=False
        )
        user.save()
        send_verification_email(user)
        flash('Your account has been created. Check your email for verification instructions', 'success')
        return redirect(url_for('frontend.home'))
    return render_template('signup.html', form=form)


