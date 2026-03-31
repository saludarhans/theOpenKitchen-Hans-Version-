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
app.config['SLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SLALCHEMY_TRACK_MODIFICATIONS"] = True

#Creates database connection and associate with the flask application

db = SQLAlchemy(app)

# dictionary of cities with their population
#cities =[]

from app import routes,models
