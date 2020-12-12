import unittest
from runningapp.resources.functions import (
    BmiCalculatorFunctions,
    CaloricNeedsCalculatorFunctions,
)


# python3.8 -m unittest runningapp/tests/resources/test_functions.py

caloric_needs_functions = CaloricNeedsCalculatorFunctions()
bmi_functions = BmiCalculatorFunctions()


class FunctionsTests(unittest.TestCase):
    def test_calculate_bmi_success(self):
        """Test if BMI is calculated correctly."""
        height = 165
        weight = 58
        bmi = bmi_functions.calculate_bmi(height, weight)
        expected_bmi = 21.3
        self.assertEqual(bmi, expected_bmi)

    def test_calculate_bmi_failure(self):
        """Test if BMI is calculated incorrectly."""
        height = 165
        weight = 58
        bmi = bmi_functions.calculate_bmi(height, weight)
        wrong_bmi = 21
        self.assertNotEqual(bmi, wrong_bmi)

    def test_calculate_activity_factor_success(self):
        """Test if the activity factor is calculated correctly."""
        trainings_per_week = 5
        activity_factor = caloric_needs_functions._calculate_activity_factor(
            trainings_per_week
        )
        expected_activity_factor = 1.8
        self.assertEqual(activity_factor, expected_activity_factor)

    def test_calculate_activity_factor_failure(self):
        """Test if the activity factor is calculated incorrectly."""
        trainings_per_week = 5
        activity_factor = caloric_needs_functions._calculate_activity_factor(
            trainings_per_week
        )
        wrong_activity_factor = 2
        self.assertNotEqual(activity_factor, wrong_activity_factor)

    def test_calculate_daily_caloric_needs_success(self):
        """Test if the daily caloric needs is calculated correctly."""
        trainings_per_week = 5
        weight = 58
        height = 165
        gender = "Female"
        age = 25

        daily_cal = caloric_needs_functions.calculate_daily_caloric_needs(
            age, height, weight, gender, trainings_per_week
        )
        expected_daily_cal = 2504

        self.assertEqual(daily_cal, expected_daily_cal)

    def test_calculate_daily_caloric_needs_failure(self):
        """Test if the daily caloric needs is calculated incorrectly."""
        trainings_per_week = 5
        weight = 58
        height = 165
        gender = "Female"
        age = 25

        daily_cal = caloric_needs_functions.calculate_daily_caloric_needs(
            age, height, weight, gender, trainings_per_week
        )
        wrong_daily_cal = 2200

        self.assertNotEqual(daily_cal, wrong_daily_cal)


if __name__ == "__main__":
    unittest.main()
