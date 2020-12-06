import unittest
from runningapp.resources.functions import (
    calculate_met_value,
    calculate_calories_burnt,
    calculate_bmi,
    calculate_activity_factor,
    calculate_average_tempo
)


# python3.8 -m unittest runningapp/tests/resources/test_functions.py


class FunctionsTests(unittest.TestCase):
    def test_calculate_met_value_success(self):
        """Test if the met value is calculated correctly"""
        tempo = 15
        met = calculate_met_value(tempo)
        expected_met = 13
        self.assertEqual(met, expected_met)

    def test_calculate_met_value_failure(self):
        """Test if the met value is calculated incorrectly"""
        tempo = 15
        met = calculate_met_value(tempo)
        wrong_met = 12
        self.assertNotEqual(met, wrong_met)

    def test_calculate_calories_burnt_success(self):
        """Test if calories burnt during 1 training are calculated correctly"""
        weight = 70
        tempo = 15
        time_in_seconds = 1800
        calories_burnt = calculate_calories_burnt(weight, tempo, time_in_seconds)
        expected_calories_burnt = 477
        self.assertEqual(calories_burnt, expected_calories_burnt)

    def test_calculate_calories_burnt_failure(self):
        """Test if calories burnt during 1 training are calculated incorrectly"""
        weight = 70
        tempo = 15
        time_in_seconds = 1800
        calories_burnt = calculate_calories_burnt(weight, tempo, time_in_seconds)
        wrong_calories_burnt = 400
        self.assertNotEqual(calories_burnt, wrong_calories_burnt)

    def test_calculate_bmi_success(self):
        """Test if BMI is calculated correctly."""
        height = 165
        weight = 58
        bmi = calculate_bmi(height, weight)
        expected_bmi = 21.3
        self.assertEqual(bmi, expected_bmi)

    def test_calculate_bmi_failure(self):
        """Test if BMI is calculated incorrectly."""
        height = 165
        weight = 58
        bmi = calculate_bmi(height, weight)
        wrong_bmi = 21
        self.assertNotEqual(bmi, wrong_bmi)

    def test_calculate_activity_factor_success(self):
        """Test if the activity factor is calculated correctly."""
        trainings_per_week = 5
        activity_factor = calculate_activity_factor(trainings_per_week)
        expected_activity_factor = 1.8
        self.assertEqual(activity_factor, expected_activity_factor)

    def test_calculate_activity_factor_failure(self):
        """Test if the activity factor is calculated incorrectly."""
        trainings_per_week = 5
        activity_factor = calculate_activity_factor(trainings_per_week)
        wrong_activity_factor = 2
        self.assertNotEqual(activity_factor, wrong_activity_factor)

    def test_calculate_average_tempo_success(self):
        """Test if the average tempo during a training is calculated correctly."""
        time_in_seconds = 1800
        distance = 7
        avg_tempo = calculate_average_tempo(time_in_seconds, distance)
        self.assertEqual(avg_tempo, 14)

    def test_calculate_average_tempo_failure(self):
        """Test if the average tempo during a training is calculated incorrectly."""
        time_in_seconds = 1800
        distance = 7
        avg_tempo = calculate_average_tempo(time_in_seconds, distance)
        self.assertNotEqual(avg_tempo, 28)


if __name__ == "__main__":
    unittest.main()
