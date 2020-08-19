from runningapp.db import db
from typing import List


class UserModel(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_staff = db.Column(db.Boolean, default=False)

    user_profile = db.relationship("UserProfileModel", lazy="dynamic")
    trainings = db.relationship("TrainingModel", lazy="dynamic")

    def save_to_db(self) -> None:
        """Save the user in the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Delete the user from the database"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        """Find the user by username"""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id: int) -> "UserModel":
        """Find the user by id"""
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        """Find all users"""
        return cls.query.all()


class UserProfileModel(db.Model):
    """User profile model"""

    __tablename__ = "user_profiles"
    __table_args__ = (db.CheckConstraint('gender="Female" OR gender="Male"'),)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    user = db.relationship("UserModel")

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(), default="Male")
    age = db.Column(db.Integer, default=25)
    height = db.Column(db.Float(precision=2), default=185)
    weight = db.Column(db.Float(precision=2), default=70)

    bmi = db.Column(db.Float(precision=2), default=0)
    daily_cal = db.Column(db.Integer, default=0)

    trainings_number = db.Column(db.Integer, default=0)
    kilometers_run = db.Column(db.Integer, default=0)

    def save_to_db(self) -> None:
        """Save the user profile in the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Delete the user profile from the database"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> "UserProfileModel":
        """Find the user profile by username"""
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return cls.query.filter_by(user_id=user.id).first()

    @classmethod
    def find_by_user_id(cls, user_id: int) -> "UserProfileModel":
        """Find the user profile by user id"""
        user = UserModel.query.filter_by(id=user_id).first()
        if user:
            return cls.query.filter_by(user_id=user.id).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserProfileModel":
        """Find the user profile by id"""
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["UserProfileModel"]:
        """Find all user profiles"""
        return cls.query.all()
