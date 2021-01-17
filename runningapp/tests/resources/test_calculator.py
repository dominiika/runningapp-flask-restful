import json
import unittest
from runningapp import create_app
from runningapp.tests.base_classes import BaseApp


class CalculatorTest(unittest.TestCase, BaseApp):
    """Test calculators"""

    def setUp(self) -> None:
        """Create a test app and a test client"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)

    def test_calculates_bmi_correctly(self):
        self.__given_test_data_is_prepared()

        self.__when_post_request_is_sent("bmi")

        self.__then_status_code_is_201_created()
        self.__then_expected_bmi_is_returned()

    def __then_expected_bmi_is_returned(self):
        expected_bmi = 34.6
        self.assertEqual(self.response.json["bmi"], expected_bmi)

    def __then_status_code_is_201_created(self):
        self.assertEqual(self.response.status_code, 201)

    def __when_post_request_is_sent(self, path):
        self.response = self.client.post(
            path=f"/{path}",
            data=json.dumps(self.data),
            headers={"Content-Type": "application/json"},
        )

    def __given_test_data_is_prepared(self):
        self.data = {"height": 170, "weight": 100}

    def test_returns_caloric_needs_correctly(self):
        self.__given_caloric_needs_data_is_prepared()

        self.__when_post_request_is_sent("daily-calories")

        self.__then_status_code_is_201_created()
        self.__then_expected_caloric_needs_are_returned()

    def __then_expected_caloric_needs_are_returned(self):
        expected_caloric_needs = 2512
        self.assertEqual(
            self.response.json["daily_caloric_needs"], expected_caloric_needs
        )

    def __given_caloric_needs_data_is_prepared(self):
        self.data = {
            "height": 170,
            "weight": 58,
            "age": 26,
            "gender": "Female",
            "trainings_per_week": 5,
        }


if __name__ == "__main__":
    unittest.main()
