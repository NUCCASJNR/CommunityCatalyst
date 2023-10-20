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
    :return: The User object
    """
    form = request.get_json()
    if not form:
        return jsonify({"error": "Not a JSON"})
    
    # Check for required fields
    required_fields = ["username", "email", "password", "first_name", "last_name", "verification_code"]
    for field in required_fields:
        if field not in form:
            return jsonify({"error": f"Missing {field}"})
    
    # Hash the password
    hashed_password = User.hash_password(form["password"])
    
    # Create a new User object
    user = User(
        username=form["username"],
        email=form["email"],
        password=hashed_password,
        first_name=form["first_name"],
        last_name=form["last_name"],
        verification_code=form["verification_code"]
    )
    
    # Save the user to the database
    user.save()
    
    return jsonify(user.to_dict())


@api.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str) -> Response | tuple[Response, int]:
    """
    Updates a user's details
    :param user_id: The id of the user to be updated
    :return: The updated user object in dict format
    """
    user = User.get(user_id)
    form = request.get_json()
    if not form:
        return jsonify({"error": "Not a json"})
    keys_ignore = ["id", "created_at", "updated_at"]

    if user:
        for key, value in form.items():
            if key not in keys_ignore:
                if key == 'password':
                    hashed_password = User.hash_password(value)
                    setattr(user, key, hashed_password)
                else:
                    setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 201
    abort(404)

