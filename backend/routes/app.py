from routes import *
from flask import jsonify, Response
from models.base_model import app, db
from flask_bcrypt import Bcrypt
from flask_cors import CORS
app.register_blueprint(donald)

bcrypt = Bcrypt(app)
CORS(app)
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