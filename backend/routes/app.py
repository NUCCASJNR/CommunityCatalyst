from routes import frontend
from flask import jsonify, Response
from models.base_model import app
from models.user import User
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login  import LoginManager
from flask_wtf.csrf import CSRFProtect, generate_csrf



CORS(app)
CORS(app, supports_credentials=True, expose_headers=["X-CSRFToken"], resources={r"/*": {"origins": "http://localhost:5173/", "allow_headers": "X-CSRFToken"}})

app.register_blueprint(frontend)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
csrf = CSRFProtect(app) 
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 
@app.errorhandler(404)
def error(error) -> Response:
    """
    404 error handler
    """
    return jsonify({"error": "Not found"})

@app.route('/get-token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    return jsonify({'X-CSRFToken': token})

@app.errorhandler(403)
def forbidden_err(error):
    """403 err handler"""
    return jsonify({"error": "unauthorized"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)