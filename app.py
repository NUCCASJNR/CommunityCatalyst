from flask import jsonify, Response, render_template, session
from models.base_model import app, db  # Assuming 'db' is your SQLAlchemy instance
from models.user import User
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from models.project import Project
from flask_login import LoginManager
from flask_cors import CORS
from routes import frontend
import logging
from flask_wtf.csrf import CSRFProtect, generate_csrf
from utils.redis_client import RedisClient

app.register_blueprint(frontend)
csrf = CSRFProtect(app)
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
    return jsonify({"error": "Unauthorized"})


@app.route("/")
def index():
    project = Project(target_amount=1000, current_amount=500)
    return render_template("index.html", project=project)


@app.route('/token', methods=['GET'])
def token():
    csrf_token = generate_csrf()
    session['csrf_token'] = csrf_token
    session.modified = True
    return jsonify({'X-CSRFToken': csrf_token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
