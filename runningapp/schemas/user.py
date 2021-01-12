from runningapp.ma import ma
from runningapp.models.user import UserModel, UserProfileModel
from marshmallow import fields, validate, Schema


class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    """Schema for User Profile"""

    gender = fields.Str(validate=[validate.OneOf(("Male", "Female"))])

    class Meta:
        model = UserProfileModel
        dump_only = ("id", "bmi", "daily_cal", "trainings_number", "kilometers_run")

        load_instance = True
        include_fk = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    """Schema for User"""

    user_profile = ma.Nested(UserProfileSchema, many=True)

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)

        load_instance = True
        include_fk = True


class ChangePasswordSchema(Schema):
    """Schema for Change Password"""

    old_password = fields.Str()
    new_password = fields.Str()


class UpdateCaloricNeedsSchema(Schema):
    """Schema for UpdateDailyCaloricNeeds"""

    daily_cal = fields.Integer()
