from flask import Blueprint

donald = Blueprint('donald', __name__, url_prefix='/')

from routes.signup import *
