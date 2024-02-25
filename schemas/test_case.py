from models.test_case import TestCaseModel

# from marshmallow import Schema, fields
from ma import ma
from models import *


class TestCaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TestCaseModel
        # load_only = ("user",)
        dump_only = ("id",)
        load_instance = True
        include_relationships = True
        include_fk = True