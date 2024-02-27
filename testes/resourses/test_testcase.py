import json

from models.test_case import TestCaseModel
from testes.base_test import BaseTest
from app import app


class TestCaseTest(BaseTest):

    def test_create_test_case(self):
        with app.app_context():

            # Generate authentication token
            auth_token, user_id = self.get_auth_token('test_user', '123456')
            test_case_data = {'title': 'Test Case 1', 'description': 'Description for Test Case 1',
                              'user_id': user_id}
            response = self.app.post('/new_testcases', json=test_case_data,
                                     headers={'Authorization': f'Bearer {auth_token}'})

            # Assert that the test case was created successfully
            self.assertEqual(response.status_code, 201, "Test case creation failed")
            self.assertEqual(TestCaseModel.query.count(), 1, "Incorrect number of test cases after creation")

            # Test retrieving the created test case with authentication headers
            response = self.app.get('/testcase/1', headers={'Authorization': f'Bearer {auth_token}'})

            # Assert that the test case data matches the expected values
            self.assertEqual(response.status_code, 200, "Failed to retrieve the created test case")
            test_case = json.loads(response.data)
            self.assertEqual(test_case['title'], 'Test Case 1', "Incorrect test case title")

    def test_get_test_cases(self):
        with app.app_context():
            test_case_1 = TestCaseModel(title='Test Case 1', description='Description for Test Case 1', user_id=1)
            test_case_2 = TestCaseModel(title='Test Case 2', description='Description for Test Case 2', user_id=1)
            test_case_1.save_to_db()
            test_case_2.save_to_db()

            auth_token, user_id = self.get_auth_token('test_user', '123456')

            response = self.app.get('/testcases', headers={'Authorization': f'Bearer {auth_token}'})
            self.assertEqual(response.status_code, 200)

    def test_update_test_case(self):
        auth_token, user_id = self.get_auth_token('test_user', '123456')
        # Create an initial test case in the database
        initial_test_case = TestCaseModel(title='Initial Title', description='Initial Description', user_id=user_id)
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
        auth_token, user_id = self.get_auth_token('test_user', '123456')

        # Create an initial test case in the database
        test_case = TestCaseModel(title='Test Case to Delete', description='Description for Test Case to Delete',
                                  user_id=user_id)
        with app.app_context():
            test_case.save_to_db()
            test_case_id = test_case.id

            response = self.app.delete(f'/testcase/{test_case_id}', headers={'Authorization': f'Bearer {auth_token}'})
            self.assertEqual(response.status_code, 200)

            # Check that the test case was deleted from the database
            deleted_test_case = TestCaseModel.find_by_id(test_case_id)
            self.assertIsNone(deleted_test_case)

    def test_invalid_request(self):
        # Test handling invalid request
        response = self.app.post('/testcases', data={})
        self.assertEqual(response.status_code, 405)
        error_message = json.loads(response.data)['message']
        self.assertEqual(error_message, 'The method is not allowed for the requested URL.')

    def test_nonexistent_test_case(self):
        # Test handling request for a nonexistent test case
        auth_token, user_id = self.get_auth_token('test_user', '123456')
        response = self.app.get('/testcase/100', headers={'Authorization': f'Bearer {auth_token}'})
        self.assertEqual(response.status_code, 404)
        error_message = json.loads(response.data)['message']
        self.assertEqual(error_message, 'Test Case is not found')
