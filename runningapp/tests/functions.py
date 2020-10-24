from werkzeug.security import generate_password_hash, check_password_hash
import json
from runningapp.models.training import TrainingModel
from runningapp.models.user import UserModel, UserProfileModel
from createsuperuser import Superuser


def set_up_test_app(obj, create_app):
    """Set up a test app"""
    obj.app = create_app()
    obj.app.app_context().push()
    obj.ctx = obj.app.test_request_context("/")
    obj.ctx.push()
    return obj.app


def set_up_client(obj):
    """Set up a client for tests"""
    obj.client = obj.app.test_client()
    obj.client.testing = True
    return obj.client


def set_up_test_db(db):
    """Set up a test database"""
    db.session.close()
    db.drop_all()
    db.create_all()


def sample_training(user: "UserModel", name: str = "test") -> "TrainingModel":
    """Create a sample training"""
    training = TrainingModel(
        name=name, user_id=user.id, distance=10, avg_tempo=8, time_in_seconds=3600
    )
    training.save_to_db()
    return training


def sample_user(username: str = "testuser") -> "UserModel":
    """Create a sample user"""
    user = UserModel(username=username, password=generate_password_hash("testpass"))
    user.save_to_db()
    user_profile = UserProfileModel(user_id=user.id)
    user_profile.save_to_db()
    return user


def get_access_token(client, username: str = "testuser", password="testpass") -> str:
    """Get the access token for the user with the given credentials"""
    data = {"username": username, "password": password}
    response = client.post(
        path="/login",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    return response.json["access_token"]


def sample_admin(username: str = "admin") -> "Superuser":
    """Create a sample admin"""
    superuser = Superuser(username, password="testpass")
    superuser.create_admin()
    return superuser
