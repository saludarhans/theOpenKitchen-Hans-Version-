
from flask import Flask

# New imports
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ
import os

# force loading of environment variables
load_dotenv('.flaskenv')

DB_NAME = environ.get('SQLITE_DB')
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csc33O'
app.config['WTF_CSRF_ENABLED'] = False
DB_CONFIG_STR = 'sqlite:///' + os.path.join(basedir, DB_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Create database connection and associate it with the Flask application
db = SQLAlchemy(app)

# Add models
from app import routes, models

"""OLD
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_doentv
from os import environ
import os

load_dotenv('.flaskenv')

DB_NAME = environ.get(SQLITE_DB)
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY']= 'csc330'
#app.config['SECRET_KEY']= 'csc330 spring 2025' Old

DB_CONFIG_STR = 'sqlite:///' + os.path.join(basedir, DB_NAME)
app.config['SQALCHEMY_DATABASE_URl'] = DB_CONFIG_STR
app.config["SQALCHEMY_TRACK_MODIFICATIONS"] = True

#Creates database connection and associate with the flask application

db = SQLAlchemy(app)

# dictionary of cities with their population
#cities =[]

from app import routes,models
"""
