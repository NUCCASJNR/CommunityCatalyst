#!/usr/bin/env python3

from flask import (
    abort,
    jsonify,
    request,
    Response
)
from api.v1 import api
from models.project import Project, User


@api.route('/projects', methods=['GET'], strict_slashes=False)
def get_all_projects() -> tuple[Response, int]:
    """Returns all projects"""
    projects = Project.all()
    projects_list = [project.to_dict() for project in projects]
    return jsonify(projects_list), 200


@api.route('/projects/u/<user_id>', methods=['GET'], strict_slashes=False)
def get_all_user_project(user_id) -> Response:
    """Returns all the projects of a user"""
    user_project = Project.find_obj_by(user_id=user_id)
    if user_project:
        return jsonify(user_project.to_dict())
    abort(404)


@api.route('/projects/u/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_all_user_project(user_id: str) -> Response:
    """
    Deletes all the projects linked to a user
    :param user_id: user_id provided
    :return:
        {}
    """
    user_project = Project.find_obj_by(user_id=user_id)
    if user_project:
        Project.delete()
        return jsonify({})
    abort(404)


@api.route('/projects/u/<user_id>/p/<project_id>',
           methods=['GET'], strict_slashes=False)
def get_a_user_project(user_id, project_id) -> Response:
    """
    GEts
    :param user_id: user_id provided
    :param project_id: project_id provided
    :return:
        The user obj if both conditions
        Abort(404) if else
    """
    user_obj = {"id": project_id, "user_id": user_id}
    print(user_obj)
    user_project = Project.find_user_by(**user_obj)
    if user_project:
        return jsonify(user_project.to_dict())
    abort(404)


@api.route('/projects/u/<user_id>/p/'
           '<project_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_specific_user_project(user_id: str, project_id: str) -> Response:
    """
    Deletes a specific user subject
    :param user_id: user_id provided
    :param project_id: project_id provided
    :return:
        An Empty dict {}
    """
    user_obj = {"id": project_id, "user_id": user_id}
    user_project = Project.find_user_by(**user_obj)
    if user_project:
        Project.delete()
        return jsonify({})
    abort(404)


@api.route('/projects/p/<project_id>',
           methods=['GET'], strict_slashes=False)
def get_project_by_id(project_id) -> Response:
    """Returns all the projects of a user"""
    project = Project.find_obj_by(id=project_id)
    if project:
        return jsonify(project.to_dict())
    abort(404)


@api.route('/projects/p/<project_id>',
           methods=['DELETE'], strict_slashes=False)
def delete_project_by_id(project_id) -> Response:
    """Returns all the projects of a user"""
    project = Project.find_obj_by(id=project_id)
    if project:
        Project.delete()
        return jsonify({})
    abort(404)


@api.route('/projects', methods=['POST'], strict_slashes=False)
def add_new_project():
    """
    Adds a new project to the projects table
    :return:
        The inserted project Obj
    """
    form = request.get_json()
    if not form:
        return jsonify({"error": "Not a JSON"})
    user_id = form['user_id']
    filtered_user = User.find_obj_by(id=user_id)
    if not filtered_user:
        return jsonify({"error":
                        "The user_id provided isn't linked to any user"})
    if not user_id:
        return jsonify({"error": "Missing user id"})
    if "title" not in form:
        return jsonify({"error": "Missing project title"})
    if "description" not in form:
        return jsonify({"error": "Missing project description"})
    if "goal_amount" not in form:
        return jsonify({"error": "Missing Project goal amount"})
    if "current_amount" not in form:
        return jsonify({"error": "Missing project current amount"})
    # if "start_date" not in form:
    #     return jsonify({"error": "Missing project start date"})
    project = Project()
    for key, value in form.items():
        setattr(project, key, value)
    project.save()
    return jsonify(project.to_dict())


@api.route('/projects/<user_id>/<project_id>',
           methods=['PUT'], strict_slashes=False)
def update_project(user_id: str, project_id: str):
    """
    Updates a project based on the project_id provided
    :param user_id:
    :param project_id: project_id provided
    :return:
        The updated project obj
    """
    keys_ignore = ["id", "created_at", "updated_at"]
    form = request.get_json()
    if not form:
        return jsonify({"error": "Not a json"})
    project_obj = {"user_id": user_id, "id": project_id}
    project = Project.find_obj_by(**project_obj)
    if project:
        for key, value in form.items():
            if key not in keys_ignore:
                setattr(project, key, value)
        project.save()
        return jsonify(project.to_dict())
    abort(404)
