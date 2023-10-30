#!/usr/bin/env python3

from api.v1 import *
from flask import jsonify, Response
from flask_migrate import Migrate
from config import app, db

app.register_blueprint(api)
migrate = Migrate(app, db)


@app.errorhandler(404)
def error(error) -> Response:
    """
    404 error handler
    """
    return jsonify({"error": "Not found"})


@app.errorhandler(403)
def forbidden_err(error):
    """403 err handler"""
    return jsonify({"error": "unauthorized"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
