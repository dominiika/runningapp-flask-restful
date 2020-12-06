from flask_restful import Resource
from flask import request
from runningapp.schemas.calculator import BmiCalculatorSchema, CaloricNeedsSchema
from runningapp.resources.functions import BmiCalculatorFunctions, CaloricNeedsCalculatorFunctions


bmi_schema = BmiCalculatorSchema()
caloric_needs_schema = CaloricNeedsSchema()
caloric_needs_functions = CaloricNeedsCalculatorFunctions()
bmi_functions = BmiCalculatorFunctions()


class BmiCalculator(Resource):
    """BMI Calculator resource"""

    @classmethod
    def post(cls):
        """Post method"""
        bmi_json = bmi_schema.load(request.get_json())
        bmi = round(bmi_functions.calculate_bmi(bmi_json["height"], bmi_json["weight"]), 1)
        return {"bmi": bmi}, 201


class CaloricNeedsCalculator(Resource):
    """Daily Caloric Needs Calculator resource"""

    @classmethod
    def post(cls):
        """Post method"""
        caloric_needs_json = caloric_needs_schema.load(request.get_json())
        caloric_needs = caloric_needs_functions.calculate_daily_caloric_needs(
            caloric_needs_json["age"],
            caloric_needs_json["height"],
            caloric_needs_json["weight"],
            caloric_needs_json["gender"],
            caloric_needs_json["trainings_per_week"],
        )
        return {"daily_caloric_needs": caloric_needs}, 201
