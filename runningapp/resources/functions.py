class BmiCalculatorFunctions:
    def calculate_bmi(self, height, weight) -> float:
        """Calculate BMI - a measure of body fat based on height and weight"""
        return round(weight / (height / 100) ** 2, 1)


class CaloricNeedsCalculatorFunctions:
    def calculate_daily_caloric_needs(
        self, age, height, weight, gender, trainings_per_week
    ) -> int:
        """Calculate BMR (Basal Metabolic Rate) - the amount of calories required for a person per day"""
        bmr = 0
        activity_factor = self._calculate_activity_factor(trainings_per_week)
        if gender == "Female":
            bmr = 655 + 9.6 * weight + 1.8 * height - 4.7 * age
        elif gender == "Male":
            bmr = 66 + 13.8 * weight + 5 * height - 6.8 * age
        daily_caloric_needs = bmr * activity_factor
        return int(daily_caloric_needs)

    def _calculate_activity_factor(self, trainings_per_week) -> int:
        """Calculate the physical activity factor based on the amount of trainings per week"""
        activity_factor_dict = {
            0: 1,
            1: 1.2,
            2: 1.4,
            3: 1.6,
            4: 1.6,
            5: 1.8,
            6: 2,
            7: 2,
        }
        return activity_factor_dict[trainings_per_week]
