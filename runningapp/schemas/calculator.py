from runningapp.ma import ma
from marshmallow import fields, Schema, validate


class BmiCalculatorSchema(ma.SQLAlchemyAutoSchema):
    """Schema for BMI Calculator"""

    weight = fields.Float(required=True)
    height = fields.Float(required=True)


class CaloricNeedsSchema(Schema):
    """Schema for Daily Caloric Needs Calculator"""

    weight = fields.Float(required=True)
    height = fields.Float(required=True)
    age = fields.Integer(required=True)
    gender = fields.Str(
        validate=[validate.OneOf(("Male", "Female"))], required=True
    )
    trainings_per_week = fields.Integer(required=True)
