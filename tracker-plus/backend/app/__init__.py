from flask import Flask
from flask_cors import CORS
from .database import db


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)

    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tracker.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)
    db.init_app(app)

    from .routes import register_routes
    register_routes(app)

    return app
