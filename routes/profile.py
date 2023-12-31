from flask import flash, redirect, url_for, request, render_template

from config import db
from forms.profile import ProfileForm
from models.user import User
from routes import frontend
from flask_login import login_required, current_user
from routes.utils import save_picture


@frontend.route('/profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = save_picture(form.picture.data, 'profile_pics')
            current_user.profile_picture = picture_filename
        current_user.first_name = form.first_name.data
        current_user.middle_name = form.middle_name.data
        current_user.last_name = form.last_name.data
        current_user.gender = form.gender.data
        current_user.birthday = form.birthday.data
        current_user.phone_number = form.contact.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.username = form.username.data
        current_user.password = User.hash_password(form.password.data)
        db.session.commit()
        flash('Your account has been successfully updated', 'success')
        return redirect(url_for('frontend.update_profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.middle_name.data = current_user.middle_name
        form.last_name.data = current_user.last_name
        form.gender.data = current_user.gender
        form.birthday.data = current_user.birthday
        form.contact.data = current_user.phone_number
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.username.data = current_user.username
    image_file = url_for('static', filename='img/profile_pics/{}'.format(current_user.profile_picture))
    return render_template('profile.html', form=form, image_file=image_file)
