from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
import datetime
from runningapp.models.user import UserModel, UserProfileModel
from runningapp.schemas.user import (
    UserSchema,
    UserProfileSchema,
    ChangePasswordSchema,
    UpdateCaloricNeedsSchema,
)
from runningapp.blacklist import BLACKLIST


user_schema = UserSchema()
user_profile_schema = UserProfileSchema()
change_password_schema = ChangePasswordSchema()
daily_needs_schema = UpdateCaloricNeedsSchema()


class User(Resource):
    """User resource"""

    @classmethod
    def get(cls, user_id: int):
        """Get method"""
        user = UserModel.find_by_id(user_id)
        if user:
            return user_schema.dump(user), 200
        return {"message": "User not found"}, 404

    @classmethod
    @jwt_required
    def delete(cls, user_id: int):
        """Delete method"""
        current_user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404
        if current_user_id != user_id:
            return (
                {
                    "message": "You don't have permission to perform this action."
                },
                403,
            )
        user_profile = UserProfileModel.find_by_user_id(user_id)
        user_profile.delete_from_db()
        user.delete_from_db()
        return {"message": "User deleted."}, 200


class UserList(Resource):
    """User List resource"""

    @classmethod
    def get(cls):
        """Get method"""
        return (
            {
                "users": [
                    user_schema.dump(user) for user in UserModel.find_all()
                ]
            },
            200,
        )


class UserProfile(Resource):
    """User Profile resource"""

    @classmethod
    @jwt_required
    def put(cls, userprofile_id: int):
        """Put method"""
        user_profile = UserProfileModel.find_by_id(userprofile_id)
        if not user_profile:
            return {"message": f"User profile not found."}, 404

        current_user_id = get_jwt_identity()

        if userprofile_id != current_user_id:
            return (
                {
                    "message": "You don't have permission to perform this action."
                },
                403,
            )

        user_profile_data = user_profile_schema.load(request.get_json())
        user_profile.gender = user_profile_data.gender
        user_profile.age = user_profile_data.age
        user_profile.height = user_profile_data.height
        user_profile.weight = user_profile_data.weight
        user_profile.calculate_bmi()

        try:
            user_profile.save_to_db()
        except:
            return (
                {"message": "An error has occurred updating the user profile."},
                500,
            )

        return user_profile_schema.dump(user_profile), 200


class UserRegister(Resource):
    """User Register resource"""

    @classmethod
    def post(cls):
        """Post method"""
        user_data = user_schema.load(request.get_json())

        if UserModel.find_by_username(user_data.username):
            return {"message": "A user with that username already exists."}, 400

        user_data.password = generate_password_hash(user_data.password)
        user_data.is_admin = False
        user_data.is_staff = False

        try:
            user_data.save_to_db()
            user = UserModel.find_by_username(user_data.username)
            user_profile = UserProfileModel(user_id=user.id)
            user_profile.save_to_db()
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(
                identity=user.id, fresh=True, expires_delta=expires
            )

        except:
            return {"message": "An error occurred creating the user."}, 500

        return (
            {
                "message": "User created successfully.",
                "access_token": access_token,
                "username": user.username,
                "user": user.id,
            },
            201,
        )


class UserLogin(Resource):
    """User Login resource"""

    @classmethod
    def post(cls):
        """Post method"""
        user_data = user_schema.load(request.get_json())
        user = UserModel.find_by_username(user_data.username)

        if user and check_password_hash(user.password, user_data.password):
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(
                identity=user.id, fresh=True, expires_delta=expires
            )

            return (
                {
                    "message": "User logged in successfully.",
                    "access_token": access_token,
                    "username": user.username,
                    "user": user.id,
                },
                200,
            )
        return {"message": "Invalid credentials."}, 401


class UserLogout(Resource):
    """User Logout resource"""

    @classmethod
    @jwt_required
    def post(cls):
        """Post method"""
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out."}, 200


class ChangePassword(Resource):
    """Change Password resource"""

    @classmethod
    @jwt_required
    def post(cls):
        """Post method"""
        current_user_id = get_jwt_identity()
        user = UserModel.find_by_id(current_user_id)
        json_data = change_password_schema.load(request.get_json())
        if check_password_hash(user.password, json_data["old_password"]):
            user.password = generate_password_hash(json_data["new_password"])
            try:
                user.save_to_db()
            except:
                return (
                    {"message": "An error has occurred updating the user."},
                    500,
                )

            return {"message": "Your password has been changed."}, 201
        return {"message": "Invalid credentials."}, 401


class UpdateCaloricNeeds(Resource):
    """Save a particular value as daily caloric needs"""

    @classmethod
    @jwt_required
    def post(cls):
        """Post method"""
        current_user_id = get_jwt_identity()
        user_profile = UserProfileModel.find_by_user_id(current_user_id)
        json_data = daily_needs_schema.load(request.get_json())

        user_profile.daily_cal = json_data["daily_cal"]
        try:
            user_profile.save_to_db()
        except:
            return {"message": "An error has occurred updating the user."}, 500

        return (
            {
                "message": "Daily caloric needs have been updated",
                "daily_cal": json_data["daily_cal"],
            },
            201,
        )
