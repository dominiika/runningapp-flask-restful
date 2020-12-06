import unittest
from runningapp import create_app
from runningapp.tests.base_classes import BaseApp, BaseUser, BaseDb, BaseTraining
from runningapp.db import db


class StatsTests(unittest.TestCase, BaseApp, BaseUser, BaseDb, BaseTraining):
    """Test stats"""

    def setUp(self) -> None:
        """Create a test app and a test client"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)
        self.user1 = self._create_sample_user(username='user1')
        self.user2 = self._create_sample_user(username='user2')

    def test_registered_users_status_code_ok(self):
        """Test if the status code is 200"""

        response = self.client.get(
            path="/total-users-number",
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 200)

    def test_registered_users_data(self):
        """Test if the data is returned correctly"""

        response = self.client.get(
            path="/total-users-number",
            headers={"Content-Type": "application/json"},
        )

        expected_number = 2

        self.assertEqual(response.json['users_number'], expected_number)

    def test_kilometers_run_code_ok(self):
        """Test if the status code is 200"""

        response = self.client.get(
            path="/total-kilometers-number",
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 200)

    def test_kilometers_run_data(self):
        """Test if the data is returned correctly"""
        self._create_sample_training(user=self.user1, distance=12)
        self._create_sample_training(user=self.user2, distance=10)

        response = self.client.get(
            path="/total-kilometers-number",
            headers={"Content-Type": "application/json"},
        )

        expected_number = 22

        self.assertEqual(response.json['kilometers_number'], expected_number)

    def test_calories_burnt_code_ok(self):
        """Test if the status code is 200"""
        pass

    def test_calories_burnt_data(self):
        """Test if the data is returned correctly"""
        pass


if __name__ == "__main__":
    unittest.main()
