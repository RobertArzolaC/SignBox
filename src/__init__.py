import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    with app.app_context():

        # set config
        app_settings = os.getenv("APP_SETTINGS")
        app.config.from_object(app_settings)

        # set up extensions
        db.init_app(app)
        login_manager.init_app(app)

        from src.models import User
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # blueprint for auth routes in our app
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth parts of app
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # shell context for flask cli
        @app.shell_context_processor
        def ctx():
            return {"app": app, "db": db}

    return app
