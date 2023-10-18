from flask import Blueprint

frontend = Blueprint('frontend', __name__, url_prefix='/')

from routes.signup import *
from routes.verify import *
from routes.common import *