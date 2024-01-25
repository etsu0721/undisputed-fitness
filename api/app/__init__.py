from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app.config import Config

# Declare extensions
db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_class=Config):
    # Initialize app
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # Blueprints
    from app.main.routes import main
    from app.exercises.routes import exercises
    app.register_blueprint(main)
    app.register_blueprint(exercises)

    return app
