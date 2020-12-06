# source: https://sites.google.com/site/compendiumofphysicalactivities/Activity-Categories/running


def calculate_calories_burnt(weight, tempo, time_in_seconds):
    """Calculate how many calories a person burnt during a training"""
    met = calculate_met_value(tempo)
    time_in_minutes = time_in_seconds / 60
    # MET * 3.5 * weight / 200 = calories/minute
    calories_burnt = met * 3.5 * weight / 200 * time_in_minutes
    return int(calories_burnt)


def calculate_met_value(tempo):
    """Calculate the metabolic equivalent of a task to measure the body's expenditure of energy"""
    met = 0
    if tempo > 22:
        met = 23
    elif 19 <= tempo <= 22:
        met = 19
    elif 17 <= tempo < 19:
        met = 16
    elif 16 <= tempo < 17:
        met = 14.5
    elif 15 <= tempo < 16:
        met = 13
    elif 12 <= tempo < 15:
        met = 12
    elif 11 <= tempo < 12:
        met = 11
    elif 9 <= tempo < 11:
        met = 10
    elif 8 <= tempo < 9:
        met = 9
    elif tempo < 8:
        met = 6
    return met


def calculate_bmi(height, weight):
    """Calculate BMI - a measure of body fat based on height and weight"""
    return round(weight / (height / 100) ** 2, 1)


def calculate_daily_caloric_needs(age, height, weight, gender, trainings_per_week):
    """Calculate BMR (Basal Metabolic Rate) - the amount of calories required for a person per day"""
    bmr = 0
    activity_factor = calculate_activity_factor(trainings_per_week)
    if gender == "Female":
        bmr = 655 + 9.6 * weight + 1.8 * height - 4.7 * age
    elif gender == "Male":
        bmr = 66 + 13.8 * weight + 5 * height - 6.8 * age
    daily_caloric_needs = bmr * activity_factor
    return int(daily_caloric_needs)


def calculate_activity_factor(trainings_per_week):
    """Calculate the physical activity factor based on the amount of trainings per week"""
    activity_factor_dict = {0: 1, 1: 1.2, 2: 1.4, 3: 1.6, 4: 1.6, 5: 1.8, 6: 2, 7: 2}
    return activity_factor_dict[trainings_per_week]


def calculate_average_tempo(time_in_seconds, distance):
    """Calculate the average tempo (km/h) during a training"""
    return round(distance/(time_in_seconds/3600), 1)
