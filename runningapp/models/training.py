from runningapp.db import db
from datetime import datetime
from typing import List
from runningapp.models.user import UserModel


class TrainingModel(db.Model):
    """Training model"""

    __tablename__ = "trainings"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    distance = db.Column(db.Float(precision=2), nullable=False)
    avg_tempo = db.Column(db.Integer, nullable=False)
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
