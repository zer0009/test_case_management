from models.test_case import TestCaseModel
from ma import ma
from models import *


class TestCaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TestCaseModel
        dump_only = ("id",)
        load_instance = True
        include_relationships = True
        include_fk = True
