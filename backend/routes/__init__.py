from flask import Blueprint

frontend = Blueprint('frontend', __name__, url_prefix='/')

from routes.signup import *
