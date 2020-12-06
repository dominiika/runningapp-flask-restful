from flask_restful import Resource
from flask import request
from runningapp.models.user import UserModel


class RegisteredUsersResource(Resource):

    @classmethod
    def get(cls):
        users_number = len(UserModel.find_all())
        return {"users_number": users_number}, 200
