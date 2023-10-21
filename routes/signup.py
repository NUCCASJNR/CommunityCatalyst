from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import current_user
from forms.signup import SignupForm
from models.user import User
from routes import frontend
from routes.utils import send_verification_email
from wtforms import ValidationError


@frontend.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Signup route
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    print("Before form validation")
    if form.validate_on_submit():
        print("Form validated successfully")
        print("Form data:", form.data)
        try:
            form.validate_username(form.username)
            form.validate_email(form.email)
        except ValidationError as e:
            flash(str(e), 'danger')
            return render_template('index.html', signupform=form)
        print("Username and email validation passed")
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
        print("User created:", user)  # Print the user object
        print("User ID:", user.id)  # Print the user's ID
        return jsonify({"success": "user created"})
    return render_template('index.html', signupform=form)


