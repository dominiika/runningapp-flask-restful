from flask_restful import Resource
from runningapp.models.training import TrainingModel
from runningapp.models.user import UserModel, UserProfileModel
from runningapp.resources.functions import TrainingCalculatorFunctions


training_functions = TrainingCalculatorFunctions()


class RegisteredUsersResource(Resource):
    @classmethod
    def get(cls):
        # refactor later:
        users_number = len(UserModel.find_all())
        return {"users_number": users_number}, 200


class KilometersRunResource(Resource):
    @classmethod
    def get(cls):
        kilometers_number = TrainingModel.get_total_kilometers()
        return {"kilometers_number": kilometers_number}, 200


class CaloriesBurntResource(Resource):
    @classmethod
    def get(cls):
        trainings = TrainingModel.find_all()
        calories_number = 0
        for training in trainings:
            user_profile = UserProfileModel.find_by_user_id(training.user.id)
            weight = user_profile.weight
            tempo = training_functions.calculate_average_tempo(
                training.time_in_seconds, training.distance
            )
            calories = training_functions.calculate_calories_burnt(
                weight, tempo, training.time_in_seconds
            )
            calories_number += calories
        return {"calories_number": calories_number}, 200
