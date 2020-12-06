import unittest
from runningapp import create_app
from runningapp.resources.stats import (
    RegisteredUsersResource
)
from runningapp.tests.base_classes import BaseApp, BaseUser, BaseDb
from runningapp.db import db


class StatsTests(unittest.TestCase, BaseApp, BaseUser, BaseDb):
    """Test stats"""

    def setUp(self) -> None:
        """Create a test app and a test client"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)

    def test_registered_users_status_code_ok(self):
        """Test if the status code is 200"""

        response = self.client.get(
            path="/users-number",
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 200)

    def test_registered_users_data(self):
        """Test if the data is returned correctly"""
        self._create_sample_user(username='test_user1')
        self._create_sample_user(username='test_user2')

        response = self.client.get(
            path="/users-number",
            headers={"Content-Type": "application/json"},
        )

        expected_number = 2

        self.assertEqual(response.json['users_number'], expected_number)


if __name__ == "__main__":
    unittest.main()
