#!/usr/bin/env python3
from typing import Tuple

from flask import (
    abort,
    jsonify,
    make_response,
    request,
    Response
)
from api.v1 import api
from models.user import User


@api.route('/users', methods=['GET'], strict_slashes=False)
def get_users() -> Response:
    """
    Retrieves all users from the database
    :return:
    """
    users = User.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@api.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id: str) -> Response:
    """
    Gets a user using the user id provided
    :param user_id: the user_id passed to the route
    :return:
        the user's details in dict format
    """
    user = User.get(user_id)
    if user:
        user_data = user.to_dict()
        return jsonify(user_data)
    abort(404)


@api.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id: str) -> Response:
    """
    Deletes a user from the users table using the id provided
    :param user_id: the user_id passed to the route
    :return:
        An empty dict if deleted
        else 404 error
    """
    user = User.get(user_id)
    if user:
        user.delete()
        return jsonify({"Status": "OK"})
    abort(404)


@api.route('/users', methods=['POST'], strict_slashes=False)
def post_new_user():
    """
    Adds a new user to the users table
    :return:
        The User obj
    """
    form = request.get_json()
    if not form:
        return jsonify({"error": "Not a json"})
    if "username" not in form:
        return jsonify({"error": "Missing username"})
    if "email" not in form:
        return jsonify({"error": "Missing email"})
    if "password" not in form:
        return jsonify({"error": "Missing password"})
    if "first_name" not in form:
        return jsonify({"error": "Missing firstname"})
    if "last_name" not in form:
        return jsonify({"error": "Missing lastname"})
    if "verification_code" not in form:
        return jsonify({"error": "Missing verification code"})
    user = User()
    for key, value in form.items():
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())


@api.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str) -> Response | tuple[Response, int]:
    """
    Updates a user's details
    :param user_id:  The id of the user to be updated
    :return:
        The updated user object in dict format
    """
    user = User.get(user_id)
    form = request.get_json()
    if not form:
        return jsonify({"error": "Not a json"})
    keys_ignore = ["id", "created_at", "updated_at"]
    if user:
        for key, value in form.items():
            if key not in keys_ignore:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 201
    abort(404)
