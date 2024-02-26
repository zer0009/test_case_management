from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.execution_result import ExecutionResultModel
from schemas.test_case import TestCaseSchema

test_case_schema = TestCaseSchema()


class NewExecutionResult(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        """This endpoint is used to create a new execution result."""
        data = request.json
        test_case_id = data.get('test_case_id')
        test_asset_id = data.get('test_asset_id')
        status = data.get('status')

        if not (test_case_id and test_asset_id and status):
            return {"message": "Missing required fields (test_case_id, test_asset_id, status)."}, 400

        try:
            execution_result = ExecutionResultModel(
                test_case_id=test_case_id,
                test_asset_id=test_asset_id,
                status=status
            )
            execution_result.save_to_db()
            return {"message": "Execution Result created successfully."}, 201
        except Exception as e:
            return {"message": "An error occurred inserting the Execution Result.", "error": str(e)}, 500


class ExecutionResult(Resource):
    @classmethod
    @jwt_required()
    def get(cls, test_asset_id: int):
        """Get execution results for a specific test asset."""
        execution_results = ExecutionResultModel.query.filter_by(test_asset_id=test_asset_id).all()
        if execution_results:
            result_list = [
                {'test_case_id': res.test_case_id, 'status': res.status,
                 'execution_time': res.execution_time.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
                 }
                for res in execution_results]
            return {'execution_results': result_list}, 200
        return {"message": "Execution results not found for the provided test asset ID."}, 404
