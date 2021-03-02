import unittest

from runningapp import create_app
from runningapp.db import db
from runningapp.models.training import TrainingModel
from runningapp.tests.base_classes import (
    BaseApp,
    BaseDb,
    BaseTraining,
    BaseUser,
)


class StatsTests(unittest.TestCase, BaseApp, BaseUser, BaseDb, BaseTraining):
    """Test stats"""

    def setUp(self) -> None:
        """Create a test app and a test client"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)
        # self.user1 = self._create_sample_user(username="user1")
        # self.user2 = self._create_sample_user(username="user2")

    def test_returns_registered_users(self):
        self.__given_users_are_created()

        self.__when_get_request_is_sent_on("/total-users-number")

        self.__then_status_code_will_be_200_ok()
        self.__then_expected_registered_users_data_will_be_returned()

    def __given_users_are_created(self):
        self.user1 = self._create_sample_user(username="user1")
        self.user2 = self._create_sample_user(username="user2")

    def __then_status_code_will_be_200_ok(self):
        self.assertEqual(self.response.status_code, 200)

    def __when_get_request_is_sent_on(self, url):
        self.response = self.client.get(
            path=url, headers={"Content-Type": "application/json"},
        )

    def __then_expected_registered_users_data_will_be_returned(self):
        expected_number = 2

        self.assertEqual(self.response.json["users_number"], expected_number)

    def test_returns_kilometers_run(self):
        self.__given_users_are_created()
        self.__given_trainings_are_created()

        self.__when_get_request_is_sent_on("/total-kilometers-number")

        self.__then_status_code_will_be_200_ok()
        self.__then_expected_kilometers_data_will_be_returned()

    def __then_expected_kilometers_data_will_be_returned(self):
        expected_number = 22

        self.assertEqual(
            self.response.json["kilometers_number"], expected_number
        )

    def __given_trainings_are_created(self):
        self._create_sample_training(
            user=self.user1, distance=12, time_in_seconds=3700
        )
        self._create_sample_training(
            user=self.user2, distance=10, time_in_seconds=3800
        )

    def test_returns_calories_burnt(self):
        self.__given_users_are_created()
        self.__given_trainings_are_created()

        self.__when_get_request_is_sent_on("/total-calories-number")

        self.__then_status_code_will_be_200_ok()
        self.__then_expected_calories_data_will_be_returned()

    def __then_expected_calories_data_will_be_returned(self):
        expected_calories = TrainingModel.calculate_total_calories()

        self.assertEqual(
            expected_calories, self.response.json["calories_number"]
        )


if __name__ == "__main__":
    unittest.main()
