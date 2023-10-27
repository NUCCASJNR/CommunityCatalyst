from flask import jsonify, Response, session
from models.base_model import app
from models.user import User
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager

from flask_cors import CORS
from routes import frontend
import logging
from flask_wtf.csrf import CSRFProtect, generate_csrf

app.register_blueprint(frontend)
csrf = CSRFProtect(app)
# Enable SQL Alchemy query logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))


@app.errorhandler(404)
def error(error) -> Response:
    return jsonify({"error": "Not found"})


@app.errorhandler(403)
def forbidden_err(error):
    return jsonify({"error": "unauthorized"})


@app.route('/token', methods=['GET'])
def token():
    # Generate a CSRF token and store it in the session
    csrf_token = generate_csrf()
    session['csrf_token'] = csrf_token
    session.modified = True  # Ensure the session is saved
    return jsonify({'X-CSRFToken': csrf_token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
