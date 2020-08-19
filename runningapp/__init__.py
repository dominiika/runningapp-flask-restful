import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from runningapp.db import db
from runningapp.ma import ma
from runningapp.blacklist import BLACKLIST
from runningapp.routes import initialize_routes
from runningapp.config import Config
from runningapp.models.user import UserModel


def create_app():
    """Create the app"""

    basedir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False
    db.init_app(app)
    ma.init_app(app)
    api = Api(app)

    @app.before_request
    def create_tables():
        """Create tables in the database"""
        db.create_all()

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validaton(err):  # except ValidationError as err
        """Handle all the validation errors"""
        return jsonify(err.messages), 400  # bad request

    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_jwt(identity):
        """Add claims to JWT token"""
        user = UserModel.find_by_id(identity)
        if user.is_admin:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        """Check if the token is in the blacklist - if the user has been logged out"""
        return (
            decrypted_token["jti"] in BLACKLIST
        )  # if True, go to revoked_token_callback

    @jwt.revoked_token_loader
    def revoked_token_callback():
        """Return unauthorized error"""
        return {"message": "You have been logged out.", "error": "token_revoked"}, 401

    initialize_routes(api)

    return app
