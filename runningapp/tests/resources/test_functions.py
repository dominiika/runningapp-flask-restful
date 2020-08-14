import unittest
from runningapp.resources.functions import (
    calculate_met_value,
    calculate_calories_burnt,
    calculate_bmi,
    calculate_activity_factor,
)


# python3.8 -m unittest runningapp/tests/resources/test_functions.py


class CalculatorsTests(unittest.TestCase):
    def test_calculate_met_value_success(self):
        """Test if the met value is calculated correctly"""
        tempo = 15
        met = calculate_met_value(tempo)
        self.assertEqual(met, 13)

    def test_calculate_met_value_failure(self):
        """Test if the met value is calculated incorrectly"""
        tempo = 15
        met = calculate_met_value(tempo)
        self.assertNotEqual(met, 12)

    def test_calculate_calories_burnt_success(self):
        """Test if calories burnt during 1 training are calculated correctly"""
        calories_burnt = calculate_calories_burnt(70, 15, 1800)
        self.assertEqual(calories_burnt, 477)

    def test_calculate_calories_burnt_failure(self):
        """Test if calories burnt during 1 training are calculated incorrectly"""
        calories_burnt = calculate_calories_burnt(70, 15, 1800)
        self.assertNotEqual(calories_burnt, 400)

    def test_calculate_bmi_success(self):
        """Test if BMI is calculated correctly."""
        bmi = calculate_bmi(165, 58)
        self.assertEqual(bmi, 21.3)

    def test_calculate_bmi_failure(self):
        """Test if BMI is calculated incorrectly."""
        bmi = calculate_bmi(165, 58)
        self.assertNotEqual(bmi, 21)

    def test_calculate_activity_factor_success(self):
        """Test if the activity factor is calculated correctly."""
        activity_factor = calculate_activity_factor(5)
        self.assertEqual(activity_factor, 1.8)

    def test_calculate_activity_factor_failure(self):
        """Test if the activity factor is calculated incorrectly."""
        activity_factor = calculate_activity_factor(5)
        self.assertNotEqual(activity_factor, 2)


if __name__ == "__main__":
    unittest.main()
