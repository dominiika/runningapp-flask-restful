from werkzeug.security import generate_password_hash
from run import app
from runningapp.models.user import UserModel, UserProfileModel


class Superuser:
    """The class can be used
    after the first request has been made
    as this action triggers database creation"""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create_admin(self):
        """Create a user model and a user profile model
        and save them to the database"""
        with app.app_context():
            hashed_pass = generate_password_hash(self.password)
            user = UserModel(
                username=self.username,
                password=hashed_pass,
                is_admin=True,
                is_staff=True,
            )
            user.save_to_db()
            user_profile = UserProfileModel(user_id=user.id)
            user_profile.save_to_db()


if __name__ == "__main__":
    admin_username = input("Choose admin username: ")
    admin_password = input("Choose admin password: ")

    superuser = Superuser(admin_username, admin_password)
    superuser.create_admin()
