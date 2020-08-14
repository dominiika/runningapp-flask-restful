import json
import unittest
from runningapp import create_app
from runningapp.tests.functions import set_up_test_app, set_up_client


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        """Create a test app and a test client"""
        set_up_test_app(obj=self, create_app=create_app)
        self.client = set_up_client(self)

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

        self.assertEqual(response.json["bmi"], 34.6)

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

        self.assertEqual(response.json["daily_caloric_needs"], 2512)


if __name__ == "__main__":
    unittest.main()
