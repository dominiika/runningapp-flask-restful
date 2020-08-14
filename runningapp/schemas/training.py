from runningapp.ma import ma
from runningapp.models.training import TrainingModel
from marshmallow import fields


class TrainingSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Training"""

    class Meta:
        model = TrainingModel
        dump_only = ("id", "user_id", "calories")
        load_instance = True
        include_fk = True

    date = fields.DateTime(format="%d-%m-%Y %H:%M:%S")
