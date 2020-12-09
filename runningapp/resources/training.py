from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from runningapp.models.training import TrainingModel
from runningapp.schemas.training import TrainingSchema
from runningapp.models.user import UserProfileModel


training_schema = TrainingSchema()
training_list_schema = TrainingSchema(many=True)


class Training(Resource):
    """Training resource"""

    @classmethod
    @jwt_required
    def get(cls, training_id: int):
        """Get method"""
        current_user_id = get_jwt_identity()
        training = TrainingModel.find_by_id(training_id)
        if training and current_user_id == training.user_id:
            return training_schema.dump(training), 200
        return {"message": "Training not found."}, 404

    @classmethod
    @jwt_required
    def delete(cls, training_id: int):
        """Delete method"""
        current_user_id = get_jwt_identity()
        user_profile = UserProfileModel.find_by_user_id(current_user_id)
        training = TrainingModel.find_by_id(training_id)
        if not training:
            return {"message": "Training not found."}, 404
        if training.user_id != current_user_id:
            return {"message": "You don't have permission to perform this action."}, 403

        user_profile.trainings_number -= 1
        user_profile.kilometers_run -= training.distance
        try:
            training.delete_from_db()
            user_profile.save_to_db()
        except:
            return {"message": "An error has occurred deleting the training."}, 500
        return {"message": "Training deleted"}, 200

    @classmethod
    @jwt_required
    def put(cls, training_id: int):
        """Put method"""
        current_user_id = get_jwt_identity()
        user_profile = UserProfileModel.find_by_user_id(current_user_id)
        training = TrainingModel.find_by_id(training_id)
        if not training:
            return {"message": "Training not found."}, 404
        if training.user_id != current_user_id:
            return {"message": "You don't have permission to perform this action."}, 403

        user_profile.kilometers_run -= training.distance
        training_data = training_schema.load(request.get_json())
        if (
            TrainingModel.find_by_name_and_user_id(training_data.name, current_user_id)
            != training
        ):
            return (
                {
                    "message": f"You have already created a training called {training_data.name}. Choose another name."
                },
                400,
            )  # bad request

        training.name = training_data.name
        training.distance = training_data.distance
        user_profile.kilometers_run += training.distance
        training.time_in_seconds = training_data.time_in_seconds
        training.calculate_average_tempo()
        training.calculate_calories_burnt()

        try:
            training.save_to_db()
            user_profile.save_to_db()
        except:
            return {"message": "An error has occurred updating the training."}, 500
        return training_schema.dump(training), 200


class TrainingList(Resource):
    """Training list resource"""

    @classmethod
    @jwt_required
    def get(cls):
        """Get method"""
        current_user_id = get_jwt_identity()
        return (
            {
                "trainings": training_list_schema.dump(
                    TrainingModel.find_all_by_user_id(current_user_id)
                )
            },
            200,
        )

    @classmethod
    @jwt_required
    def post(cls):
        """Post method"""
        training_json = request.get_json()
        current_user_id = get_jwt_identity()
        user_profile = UserProfileModel.find_by_user_id(current_user_id)
        training = TrainingModel.find_by_name_and_user_id(
            training_json["name"], current_user_id
        )
        if training:
            return (
                {
                    "message": f"You have already created a training called {training_json['name']}. Choose another name."
                },
                400,
            )  # bad request

        training = training_schema.load(training_json)
        training.user_id = current_user_id
        training.calculate_average_tempo()
        training.calculate_calories_burnt()
        user_profile.trainings_number += 1
        user_profile.kilometers_run += training.distance

        try:
            training.save_to_db()
            user_profile.save_to_db()
        except:
            return (
                {"message": "An error has occurred inserting the training."},
                500,
            )  # internal server error
        return training_schema.dump(training), 201
