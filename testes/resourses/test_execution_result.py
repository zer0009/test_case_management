from app import app
from models.execution_result import ExecutionResultModel
from models.test_case import TestCaseModel
from testes.base_test import BaseTest


class ExecutionResultTest(BaseTest):
    def test_create_execution_result(self):
        auth_token, user_id = self.get_auth_token('test_user', '123456')

        with app.app_context():
            test_case = TestCaseModel(title='Test Case 1', description='Description for Test Case 1', user_id=user_id)
            test_case.save_to_db()
            data = {'test_case_id': test_case.id, 'test_asset_id': 1, 'status': 'success'}

            response = self.app.post('/executions', json=data, headers={'Authorization': f'Bearer {auth_token}'})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(ExecutionResultModel.query.count(), 1)

    def test_get_execution_results_for_test_asset(self):
        auth_token, user_id = self.get_auth_token('test_user', '123456')

        # Create a test case
        with app.app_context():
            test_case = TestCaseModel(title='Test Case 1', description='Description for Test Case 1', user_id=user_id)
            test_case.save_to_db()

            # Create execution results for the test case
            execution_result_1 = ExecutionResultModel(test_case_id=test_case.id, test_asset_id=1, status='success')
            execution_result_2 = ExecutionResultModel(test_case_id=test_case.id, test_asset_id=2, status='failure')
            execution_result_1.save_to_db()
            execution_result_2.save_to_db()

        # Send a GET request to retrieve execution results for test asset 1
        response = self.app.get('/execution_results/1', headers={'Authorization': f'Bearer {auth_token}'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['execution_results']), 1)  # Expecting only one execution result for test asset 1

    def test_get_execution_results_not_found(self):
        auth_token, user_id = self.get_auth_token('test_user', '123456')

        # Send a GET request for a test asset that doesn't exist
        response = self.app.get('/execution_results/999', headers={'Authorization': f'Bearer {auth_token}'})
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['message'], "Execution results not found for the provided test asset ID.")

    def test_create_execution_result_missing_fields(self):
        auth_token, user_id = self.get_auth_token('test_user', '123456')

        # Missing required fields for creating an execution result
        data = {'test_case_id': 1}  # Missing test_asset_id and status
        response = self.app.post('/executions', json=data, headers={'Authorization': f'Bearer {auth_token}'})
        self.assertEqual(response.status_code, 400)

    def test_create_execution_result_unauthorized(self):
        # Create an execution result without providing authentication token
        data = {'test_case_id': 1, 'test_asset_id': 1, 'status': 'success'}

        response = self.app.post('/executions', json=data)
        self.assertEqual(response.status_code, 401)
