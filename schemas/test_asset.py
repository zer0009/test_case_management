from ma import ma
from models.test_asset import TestAssetModel


class TestAssetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TestAssetModel
        dump_only = ("id",)
        load_instance = True
        include_relationships = True
        include_fk = True
