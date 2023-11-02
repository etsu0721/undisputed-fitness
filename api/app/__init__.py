from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'c87cf4f86058cdfa763cf4d340a0908v'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.app_context().push()
ma = Marshmallow(app)

from app import routes