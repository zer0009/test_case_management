from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity

from datetime import datetime

from models.execution_result import ExecutionResultModel
from models.test_case import TestCaseModel
# from models.user import UserModel
# from schemas.execution_result import ExecutionResultSchema

from schemas.test_case import TestCaseSchema

import json

test_case_schema = TestCaseSchema()
# execution_results_schema = ExecutionResultSchema()
# fax_schema_list = FaxSchema(many=True)
# user_schema = UserSchema()
# User_schema_list = UserSchema(many=True)
# state_schema = StateSchema()


# def record_execution_result():
#     data = request.json
#     test_case_id = data.get('test_case_id')
#     test_asset_id = data.get('test_asset_id')
#     result = data.get('result')
#
#
#     db.session.add(execution_result)
#     db.session.commit()
#
#     return jsonify({'message': 'Execution result recorded successfully'}), 201
class NewExecutionResult(Resource):
    @classmethod
    # @jwt_required()
    def post(cls):
        """This endpoint is used to make new test case by the user owner."""
        data = request.json
        test_case_id = data.get('test_case_id')
        test_asset_id = data.get('test_asset_id')
        status = data.get('status')
        execution_result = ExecutionResultModel(test_case_id=test_case_id, test_asset_id=test_asset_id, status=status)

        # execution_result = execution_results_schema.load(request.get_json())
        if execution_result:
            execution_result.save_to_db()
        else:
            return {"message": "An error occurred inserting the Execution Result."}, 500
        return {"message": "Execution Result created successfully."}, 201

class ExecutionResult(Resource):

    @classmethod
    # @jwt_required()
    def get(cls, test_asset_id: int):
        """This endpoint is used for to get an specific fax by id => url/fax/4."""
        # user_id = get_jwt_identity()
        # user_id = get_jwt_identity()
        # current_user = UserModel.find_by_id(user_id)
        # res = [*set(l)]
        # claims = get_jwt()
        # if fax:
        #     if (user_id == fax.user_id) or claims["is_admin"] or (fax_id == fax_received.fax_id):
        #         return fax_schema.dump(fax), 200
        execution_results = ExecutionResultModel.query.filter_by(test_asset_id=test_asset_id).all()
        if execution_results:
            result_list = [
                {'test_case_id': res.test_case_id, 'status': res.status, 'execution_time': res.execution_time}
                for res in execution_results]
            return jsonify({'execution_results': result_list}), 200
        return {"message": "execution results is not found"}, 404



        # if test_case:
        #     return test_case_schema.dump(test_case), 200

        # return {"message": "Test Case is not found"}, 404

    # @classmethod
    # @jwt_required()
    # def delete(cls, test_case_id: int):
    #     """This endpoint is used for delete fax by the user owner of the fax or the admin."""
    #     user_id = get_jwt_identity()
    #     test_case = TestCaseModel.find_by_id(test_case_id)
    #     claims = get_jwt()
    #     if test_case:
    #         if (user_id == test_case.user_id) or claims["is_admin"]:
    #             # ReplayModel.delete_replay_by_ticket_id(ticket_id)
    #             # NoteModel.delete_note_by_fax_id(fax_id)
    #             test_case.delete_from_db()
    #             return {"message": "Test Case deleted."}
    #         return {"message": "You are not allowed."}, 404
    #     return {"message": "Test Case not found."}, 404
    #
    # @classmethod
    # @jwt_required()
    # def put(cls, test_case_id: int):
    #     """This endpoint is used for update the fax or add new fax by the owner of the fax or the admin."""
    #     user_id = get_jwt_identity()
    #     test_case = TestCaseModel.find_by_id(test_case_id)
    #     test_case_json = request.get_json()
    #     if test_case:
    #         print(test_case.user_id)
    #         if user_id == test_case.user_id:
    #             test_case.title = test_case_json["title"]
    #             test_case.body = test_case_json["body"]
    #             test_case.state = test_case_json["state"]
    #             test_case.distinction_id = test_case_json["distinction_id"]
    #     else:
    #         test_case = test_case_schema.load(test_case_json)
    #     test_case.save_to_db()
    #     return test_case_schema.dump(test_case)