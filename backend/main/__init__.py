"""
Flask object using the application factory pattern for creating.
"""

from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session

from .config import config_by_name


db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    Session(app)
    db.init_app(app)
    flask_bcrypt.init_app(app)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    
    from main.routes import user_routes, member_routes
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(member_routes.bp)

    return app