from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_claims
from runningapp.models.user import UserModel, UserProfileModel
from runningapp.schemas.user import UserSchema


user_schema = UserSchema()


class AdminManageUser(Resource):
    """Manage a user from the admin panel"""

    @classmethod
    @jwt_required
    def get(cls, user_id):
        """Get the user"""
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return (
                {
                    "message": "You don't have permission to perform this action."
                },
                403,
            )

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404
        return user_schema.dump(user), 200

    @classmethod
    @jwt_required
    def put(cls, user_id):
        """Change username, password or promote the user to be the admin or staff"""
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return (
                {
                    "message": "You don't have permission to perform this action."
                },
                403,
            )

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": f"User not found."}, 404

        user_data = user_schema.load(request.get_json())
        user.username = user_data.username
        user.password = generate_password_hash(user_data.password)
        user.is_staff = user_data.is_staff
        user.is_admin = user.is_admin

        try:
            user.save_to_db()
        except:
            return (
                {"message": "An error has occurred updating the user profile."},
                500,
            )

        return user_schema.dump(user), 200

    @classmethod
    @jwt_required
    def delete(cls, user_id):
        """Delete the user"""
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return (
                {
                    "message": "You don't have permission to perform this action."
                },
                403,
            )

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404
        user_profile = UserProfileModel.find_by_user_id(user_id)
        user_profile.delete_from_db()
        user.delete_from_db()
        return {"message": "User deleted."}, 200


class AdminManageUserList(Resource):
    """Manage the user list from the admin panel"""

    @classmethod
    @jwt_required
    def get(cls):
        """Get the user list"""
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return (
                {
                    "message": "You don't have permission to perform this action."
                },
                403,
            )

        return (
            {
                "users": [
                    user_schema.dump(user) for user in UserModel.find_all()
                ]
            },
            200,
        )

    @classmethod
    @jwt_required
    def post(cls):
        """Register a user"""
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return (
                {
                    "message": "You don't have permission to perform this action."
                },
                403,
            )

        user_data = user_schema.load(request.get_json())
        if UserModel.find_by_username(user_data.username):
            return {"message": "A user with that username already exists."}, 400

        user_data.password = generate_password_hash(user_data.password)

        try:
            user_data.save_to_db()
            user = UserModel.find_by_username(user_data.username)
            user_profile = UserProfileModel(user_id=user.id)
            user_profile.save_to_db()

        except:
            return {"message": "An error occurred creating the user."}, 500
        return {"message": "User created successfully."}, 201
