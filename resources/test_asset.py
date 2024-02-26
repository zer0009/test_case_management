from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from schemas.test_asset import TestAssetSchema

test_asset_schema = TestAssetSchema()


class NewTestAsset(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        """This endpoint is used to make new test asset by the user owner."""
        test_asset = test_asset_schema.load(request.get_json())
        if test_asset:
            test_asset.save_to_db()
        else:
            return {"message": "An error occurred inserting the test asset."}, 500
        return {"message": "test asset created successfully."}, 201

# class NewTestAsset(Resource):
#     @classmethod
#     @jwt_required()
#     def post(cls):
#         data = request.json
#         name = data.get('name')
#         test_asset = TestAssetModel(name=name)
#         if test_asset:
#             test_asset.save_to_db()
#         else:
#             return {"message": "An error occurred inserting the test asset."}, 500
#         return {"message": "Test asset created successfully."}, 201
