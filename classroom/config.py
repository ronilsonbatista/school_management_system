import os.path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

project_dir = os.path.dirname(os.path.abspath(__file__))
database_name = "classroom.db"
database_file = "sqlite:///{}".format(os.path.join(project_dir, database_name))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
