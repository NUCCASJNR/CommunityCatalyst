#!/usr/bin/env python3

from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from api.v1.comment import *
from api.v1.user import *
from api.v1.project import *
