from flask import jsonify, Response
from models.base_model import app
from models.user import User
from flask_bcrypt import Bcrypt

from flask_login import LoginManager

from routes import frontend
import logging

app.register_blueprint(frontend)
app.logger.setLevel(logging.DEBUG)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def error(error) -> Response:
    return jsonify({"error": "Not found"})


@app.errorhandler(403)
def forbidden_err(error):
    return jsonify({"error": "unauthorized"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
