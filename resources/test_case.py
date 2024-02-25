from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from models.test_case import TestCaseModel
from schemas.test_case import TestCaseSchema

test_case_schema = TestCaseSchema()
test_case_schema_list = TestCaseSchema(many=True)


class NewTestCase(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        """This endpoint is used to make new test case by the user owner."""
        test = test_case_schema.load(request.get_json())
        if test:
            test.save_to_db()
        else:
            return {"message": "An error occurred inserting the test case."}, 500
        return {"message": "test case created successfully."}, 201


class TestCase(Resource):
    @classmethod
    @jwt_required()
    def get(cls, test_case_id: int):
        """This endpoint is used for to get an specific fax by id => url/fax/4."""
        user_id = get_jwt_identity()
        test_case = TestCaseModel.find_by_id(test_case_id)
        claims = get_jwt()
        if test_case:
            if (user_id == test_case.user_id) or claims["is_admin"]:
                return test_case_schema.dump(test_case), 200

        return {"message": "Test Case is not found"}, 404

    # @classmethod
    # # @jwt_required()
    # def delete(cls, test_case_id: int):
    #     """This endpoint is used for delete fax by the user owner of the fax or the admin."""
    #     test_case = TestCaseModel.find_by_id(test_case_id)
    #     if test_case:
    #         test_case.delete_from_db()
    #         return {"message": "Test Case deleted."}
    #     return {"message": "Test Case not found."}, 404

    @classmethod
    @jwt_required()
    def delete(cls, test_case_id: int):
        """This endpoint is used for delete test case by the user owner or the admin."""
        user_id = get_jwt_identity()
        test_case = TestCaseModel.find_by_id(test_case_id)
        claims = get_jwt()
        if test_case:
            if (user_id == test_case.user_id) or claims["is_admin"]:
                test_case.delete_from_db()
                return {"message": "Test Case deleted."}
            return {"message": "You are not allowed."}, 404
        return {"message": "Test Case not found."}, 404

    @classmethod
    @jwt_required()
    def put(cls, test_case_id: int):
        """This endpoint is used for update the test case or add new test case by the user owner or the admin."""
        user_id = get_jwt_identity()
        test_case = TestCaseModel.find_by_id(test_case_id)
        test_case_json = request.get_json()
        if test_case:
            if user_id == test_case.user_id:
                test_case.title = test_case_json["title"]
                test_case.description = test_case_json["description"]
        else:
            test_case = test_case_schema.load(test_case_json)
        test_case.save_to_db()
        return test_case_schema.dump(test_case)

    # @classmethod
    # # @jwt_required()
    # def put(cls, test_case_id: int):
    #     """This endpoint is used for update the fax or add new fax by the owner of the fax or the admin."""
    #     # user_id = get_jwt_identity()
    #     test_case = TestCaseModel.find_by_id(test_case_id)
    #     test_case_json = request.get_json()
    #     if test_case:
    #         test_case.title = test_case_json["title"]
    #         test_case.description = test_case_json["description"]
    #     else:
    #         test_case = test_case_schema.load(test_case_json)
    #     test_case.save_to_db()
    #     return test_case_schema.dump(test_case)


class TestCaseList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        test_cases = TestCaseModel.find_all()
        if test_cases:
            return {"Test Cases": [test_case_schema_list.dump(test_cases)]}, 200
        # result = [{'id': test_case.id, 'name': test_case.name, 'description': test_case.description} for test_case in
        #           test_cases]
        # return jsonify(result)
