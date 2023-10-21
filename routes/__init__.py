#!/usr/bin/env python3
from flask import Blueprint

frontend = Blueprint('frontend', __name__, url_prefix='/')

from routes.signup import *
from routes.utils import *
from routes.login import *