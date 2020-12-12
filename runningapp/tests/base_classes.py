import json

from werkzeug.security import generate_password_hash

from createsuperuser import Superuser
from runningapp import UserModel
from runningapp.models.training import TrainingModel
from runningapp.models.user import UserProfileModel


class BaseApp:
    """Create base app"""

    @classmethod
    def _set_up_test_app(cls, create_app):
        """Set up a test app"""
        app = create_app()
        app.app_context().push()
        ctx = app.test_request_context("/")
        ctx.push()
        return app

    @classmethod
    def _set_up_client(cls, app):
        """Set up a client for tests"""
        client = app.test_client()
        client.testing = True
        return client


class BaseDb:
    """Create base database"""

    @classmethod
    def _set_up_test_db(cls, db) -> None:
        """Set up a test database"""
        db.session.close()
        db.drop_all()
        db.create_all()


class BaseUser:
    """Create a base user"""

    @classmethod
    def _create_sample_user(
        cls, username: str = "testuser", height=185, weight=70, gender="Male", age=25
    ) -> "UserModel":
        """Create a sample user"""
        user = UserModel(username=username, password=generate_password_hash("testpass"))
        user.save_to_db()
        user_profile = UserProfileModel(
            user_id=user.id, height=height, weight=weight, gender=gender, age=age
        )
        user_profile.save_to_db()
        return user

    @classmethod
    def _get_access_token(
        cls, client, username: str = "testuser", password="testpass"
    ) -> str:
        """Get the access token for the user with the given credentials"""
        data = {"username": username, "password": password}
        response = client.post(
            path="/login",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        return response.json["access_token"]


class BaseAdmin:
    """Create a base admin"""

    @classmethod
    def _get_admin_access_token(
        cls, client, username: str = "admin", password="testpass"
    ) -> str:
        """Get the access token for the user with the given credentials"""
        data = {"username": username, "password": password}
        response = client.post(
            path="/login",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        return response.json["access_token"]

    @classmethod
    def _create_sample_admin(cls, username: str = "admin") -> "Superuser":
        """Create a sample admin"""
        superuser = Superuser(username, password="testpass")
        superuser.create_admin()
        return superuser


class BaseTraining:
    """Create a base training"""

    @classmethod
    def _create_sample_training(
        cls,
        user: "UserModel",
        name: str = "test",
        distance: int = 10,
        time_in_seconds=3600,
    ) -> "TrainingModel":
        """Create a sample training"""
        training = TrainingModel(
            name=name,
            user_id=user.id,
            distance=distance,
            time_in_seconds=time_in_seconds,
        )
        training.calculate_average_tempo()
        training.save_to_db()
        return training
