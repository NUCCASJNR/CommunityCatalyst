#!/usr/bin/env python3
"""
Handles database configuration and loads all env variables needed
"""

from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

user = getenv("COMMUNITY_USER")
database = getenv("COMMUNITY_DB")
password = getenv("COMMUNITY_PWD")
host = getenv("COMMUNITY_HOST")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})

app.config['SECRET_KEY'] = 'sg3t312388373y122wdddffccff1'

if app.config['TESTING']:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    app.config['SQLALCHEMY_DATABASE_URI']\
        = f'mysql+mysqldb://{user}:{password}@{host}/{database}'

db = SQLAlchemy(app)
