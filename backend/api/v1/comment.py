#!/usr/bin/env python3

from flask import (
    abort,
    jsonify,
    request,
    Response
)
from api.v1 import api
from models.comment import Comment


@api.route('/comments/<project_id>', methods=['GET'], strict_slashes=False)
def get_all_comments(project_id: str) -> Response:
    """
    GEt all the comments made on a project
    :return:
        The comments
    """
    obj = {"project_id": project_id}
    comments = Comment.find_obj_by(**obj)
    print(comments)
    if comments:
        return jsonify(comments.to_dict())
    abort(404)

