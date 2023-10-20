from datetime import datetime
from flask import url_for, redirect, flash
from routes.utils import home
from flask_login import current_user, login_user

from routes import frontend
from models.user import User


# @frontend.route('/verify/<string:verification_code>', methods=['GET', 'POST'])
# def verify(verification_code):
#     """
#     Verification route
#     Verifies a user based on the verification code provided
#     """
#     if current_user.is_authenticated:
#         return redirect(url_for(home))
#     query = {'verification_code': verification_code}
#     user = User.find_obj_by(**query)
#     if user:
#         if user.verification_expires_at and datetime.utcnow() > user.verification_expires_at:
#             user.delete()
#             flash('The verification link has expired,'
#                   ' Please signup again to receive a new verification code',
#                   'danger')
#             return redirect(url_for(home))
#         user.verified = True
#         user.verification_code = None
#         login_user(user)
#         flash('Your account has successfully been created'
#               'and you have been logged in, Happy Funding', 'success')
#     else:
#         flash('Invalid verification code. Please try again', 'danger')
#     return redirect(url_for(home))