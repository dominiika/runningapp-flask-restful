import json
import unittest
from runningapp import create_app
from runningapp.tests.base_classes import BaseApp


# TODO REFACTOR ALL THE TESTS
class CalculatorTests(unittest.TestCase, BaseApp):
    """Test calculators"""

    def setUp(self) -> None:
        """Create a test app and a test client"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)

    def test_bmi_calculator_status_code(self):
        """Test if the status code is 201 if the user enters required data"""
        data = {"height": 170, "weight": 100}
        response = self.client.post(
            path="/bmi",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 201)

    def test_bmi_calculator_data(self):
        """Test if the data is returned correctly"""
        data = {"height": 170, "weight": 100}
        response = self.client.post(
            path="/bmi",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        expected_bmi = 34.6

        self.assertEqual(response.json["bmi"], expected_bmi)

    def test_caloric_needs_calculator_status_code(self):
        """Test if the status code is 201 if the user enters required data"""
        data = {
            "height": 170,
            "weight": 58,
            "age": 26,
            "gender": "Female",
            "trainings_per_week": 5,
        }
        response = self.client.post(
            path="/daily-calories",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 201)

    def test_caloric_needs_calculator_data(self):
        """Test if the data is returned correctly"""
        data = {
            "height": 170,
            "weight": 58,
            "age": 26,
            "gender": "Female",
            "trainings_per_week": 5,
        }
        response = self.client.post(
            path="/daily-calories",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        expected_caloric_needs = 2512

        self.assertEqual(response.json["daily_caloric_needs"], expected_caloric_needs)


if __name__ == "__main__":
    unittest.main()
