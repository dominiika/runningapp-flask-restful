import json

from werkzeug.security import generate_password_hash

from createsuperuser import Superuser
from runningapp import UserModel
from runningapp.models.user import UserProfileModel


class BaseApp:
    """Create base app"""

    def _set_up_test_app(self, create_app):
        """Set up a test app"""
        app = create_app()
        app.app_context().push()
        ctx = app.test_request_context("/")
        ctx.push()
        return app

    def _set_up_client(self, app):
        """Set up a client for tests"""
        client = app.test_client()
        client.testing = True
        return client


class BaseDb:
    """Create base database"""

    def _set_up_test_db(self, db) -> None:
        """Set up a test database"""
        db.session.close()
        db.drop_all()
        db.create_all()


class BaseUser:
    """Create a base user"""

    def _create_sample_user(self, username: str = "testuser") -> "UserModel":
        """Create a sample user"""
        user = UserModel(username=username, password=generate_password_hash("testpass"))
        user.save_to_db()
        user_profile = UserProfileModel(user_id=user.id)
        user_profile.save_to_db()
        return user

    def _get_access_token(
        self, client, username: str = "testuser", password="testpass"
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

    def _get_admin_access_token(
        self, client, username: str = "admin", password="testpass"
    ) -> str:
        """Get the access token for the user with the given credentials"""
        data = {"username": username, "password": password}
        response = client.post(
            path="/login",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        return response.json["access_token"]

    def _create_sample_admin(self, username: str = "admin") -> "Superuser":
        """Create a sample admin"""
        superuser = Superuser(username, password="testpass")
        superuser.create_admin()
        return superuser
