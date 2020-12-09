from runningapp.db import db
from datetime import datetime
from typing import List
from runningapp.models.user import UserModel, UserProfileModel

# source: https://sites.google.com/site/compendiumofphysicalactivities/Activity-Categories/running


class TrainingModel(db.Model):
    """Training model"""

    __tablename__ = "trainings"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    distance = db.Column(db.Float(precision=2), nullable=False)
    avg_tempo = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_in_seconds = db.Column(db.Integer, nullable=False)

    calories = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")

    def save_to_db(self) -> None:
        """Save the training in the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Delete the training from the database"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name: str) -> "TrainingModel":
        """Find the training by name"""
        return cls.query.filter_by(
            name=name
        ).first()  # SELECT * FROM trainings WHERE name=name LIMIT 1;

    @classmethod
    def find_by_name_and_user_id(cls, name: str, user_id: int) -> "TrainingModel":
        """Find the training by name and user id"""
        return cls.query.filter_by(name=name, user_id=user_id).first()

    @classmethod
    def find_by_id(cls, training_id: int) -> "TrainingModel":
        """Find the training by id"""
        return cls.query.filter_by(id=training_id).first()

    @classmethod
    def find_all(cls) -> List["TrainingModel"]:
        """Find all the trainings"""
        return cls.query.all()

    @classmethod
    def find_all_by_user_id(cls, user_id: int) -> List["TrainingModel"]:
        """Find all the trainings which belong to the logged in user"""
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_total_kilometers(cls) -> float:
        """Get total kilometers run by all the users"""
        trainings = cls.query.all()
        total_number = 0
        for training in trainings:
            total_number += training.distance
        return total_number

    def calculate_calories_burnt(self) -> None:
        """Calculate how many calories a person burnt during a training"""
        self.calculate_average_tempo()
        weight = self._get_users_weight()
        met = self._calculate_met_value()
        time_in_minutes = self.time_in_seconds / 60
        # MET * 3.5 * weight / 200 = calories/minute
        calories_burnt = met * 3.5 * weight / 200 * time_in_minutes
        self.calories = int(calories_burnt)

    def _get_users_weight(self):
        """Access user's weight by user profile"""
        user_profile = UserProfileModel.find_by_user_id(self.user_id)
        return user_profile.weight

    def _calculate_met_value(self) -> int:
        """Calculate the metabolic equivalent of a task to measure the body's expenditure of energy"""
        met = 0
        if self.avg_tempo > 22:
            met = 23
        elif 19 <= self.avg_tempo <= 22:
            met = 19
        elif 17 <= self.avg_tempo < 19:
            met = 16
        elif 16 <= self.avg_tempo < 17:
            met = 14.5
        elif 15 <= self.avg_tempo < 16:
            met = 13
        elif 12 <= self.avg_tempo < 15:
            met = 12
        elif 11 <= self.avg_tempo < 12:
            met = 11
        elif 9 <= self.avg_tempo < 11:
            met = 10
        elif 8 <= self.avg_tempo < 9:
            met = 9
        elif self.avg_tempo < 8:
            met = 6
        return met

    def calculate_average_tempo(self) -> None:
        """Calculate the average tempo (km/h) during a training"""
        self.avg_tempo = round(self.distance / (self.time_in_seconds / 3600), 1)

    @classmethod
    def calculate_total_calories(cls):
        """Calculate total calories burnt by all the users during all the trainings"""
        trainings = cls.query.all()
        calories_number = 0
        for training in trainings:
            training.calculate_calories_burnt()
            calories_number += training.calories
        return calories_number
