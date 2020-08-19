import sqlite3
from werkzeug.security import generate_password_hash


class Superuser:
    """The class can be used after the first request has been made as this action triggers database creation"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.db = "runningapp/data.db"

    def create_admin(self):
        """Create the admin"""
        self._create_user()
        self._create_user_profile()
        self._get_user_id()
        return "Superuser created successfully"

    def _create_user(self):
        """Create a record to populate the users table"""
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        query = "INSERT INTO users (username, password, is_admin, is_staff) VALUES (?, ?, ?, ?)"
        cursor.execute(
            query, (self.username, generate_password_hash(self.password), True, True)
        )
        connection.commit()
        connection.close()

    def _create_user_profile(self):
        """Create a record to populate the user_profiles table"""
        user_id = self._get_user_id()
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        query = (
            "INSERT INTO user_profiles "
            "(user_id, gender, age, height, weight, bmi, daily_cal, trainings_number, kilometers_run) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        cursor.execute(query, (user_id, "Female", 25, 170, 55, 0, 0, 0, 0))
        connection.commit()
        connection.close()

    def _get_user_id(self):
        """Find the id in the suers table to make a relation to user_profiles table possible"""
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (self.username,))
        user_id = result.fetchone()[0]
        connection.commit()
        connection.close()
        return user_id


admin_username = input("Choose admin username: ")
admin_password = input("Choose admin password: ")

superuser = Superuser(admin_username, admin_password)
superuser.create_admin()
