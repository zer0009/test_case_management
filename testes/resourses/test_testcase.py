import json

from models.execution_result import ExecutionResultModel
from models.test_case import TestCaseModel
from testes.base_test import BaseTest
from app import app


class TestCaseTest(BaseTest):
    def test_create_test_case(self):
        with app.app_context():
            data = {'title': 'Test Case 1', 'description': 'Description for Test Case 1'}
            response = self.app.post('/new_testcases', json=data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(TestCaseModel.query.count(), 1)

            # Test retrieving the created test case
            response = self.app.get('/testcase/1')
            self.assertEqual(response.status_code, 200)
            test_case = json.loads(response.data)
            self.assertEqual(test_case['title'], 'Test Case 1')

    def test_get_test_cases(self):
        with app.app_context():
            test_case_1 = TestCaseModel(title='Test Case 1', description='Description for Test Case 1')
            test_case_2 = TestCaseModel(title='Test Case 2', description='Description for Test Case 2')
            test_case_1.save_to_db()
            test_case_2.save_to_db()

            response = self.app.get('/testcases')
            self.assertEqual(response.status_code, 200)

    def test_update_test_case(self):
        # Create an initial test case in the database
        initial_test_case = TestCaseModel(title='Initial Title', description='Initial Description')
        with app.app_context():
            initial_test_case.save_to_db()

        # Define the updated values for the test case
        updated_title = 'Updated Title'
        updated_description = 'Updated Description'

        # Perform the update operation by fetching the test case from the database and updating its attributes
        with app.app_context():
            test_case_to_update = TestCaseModel.query.filter_by(title='Initial Title').first()
            test_case_to_update.title = updated_title
            test_case_to_update.description = updated_description
            test_case_to_update.save_to_db()

        # Retrieve the updated test case from the database
        with app.app_context():
            updated_test_case = TestCaseModel.query.filter_by(title=updated_title).first()

            # Assert that the test case was updated correctly
            self.assertIsNotNone(updated_test_case)
            self.assertEqual(updated_test_case.description, updated_description)

    def test_delete_test_case(self):
        # Create an initial test case in the database
        test_case = TestCaseModel(title='Test Case to Delete', description='Description for Test Case to Delete')
        with app.app_context():
            test_case.save_to_db()
            test_case_id = test_case.id

            test_case.delete_from_db()

            deleted_test_case = TestCaseModel.find_by_id(test_case_id)

            self.assertIsNone(deleted_test_case)

    def test_create_execution_result(self):
        with app.app_context():
            test_case = TestCaseModel(title='Test Case 1', description='Description for Test Case 1')
            test_case.save_to_db()

            data = {'test_case_id': test_case.id, 'test_asset_id': 1, 'status': 'success'}
            response = self.app.post('/executions', json=data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(ExecutionResultModel.query.count(), 1)

    def test_invalid_request(self):
        # Test handling invalid request
        response = self.app.post('/testcases', data={})
        self.assertEqual(response.status_code, 405)
        error_message = json.loads(response.data)['message']
        self.assertEqual(error_message, 'The method is not allowed for the requested URL.')

    def test_nonexistent_test_case(self):
        # Test handling request for a nonexistent test case
        response = self.app.get('/testcase/100')
        self.assertEqual(response.status_code, 404)
        error_message = json.loads(response.data)['message']
        self.assertEqual(error_message, 'Test Case is not found')
