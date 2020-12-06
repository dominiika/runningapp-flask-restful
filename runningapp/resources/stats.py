from flask_restful import Resource
from runningapp.models.training import TrainingModel
from runningapp.models.user import UserModel


class RegisteredUsersResource(Resource):

    @classmethod
    def get(cls):
        users_number = len(UserModel.find_all())
        return {"users_number": users_number}, 200


class KilometersRunResource(Resource):

    @classmethod
    def get(cls):
        kilometers_number = TrainingModel.get_total_kilometers()
        return {"kilometers_number": kilometers_number}, 200
