from app import app
from testes.base_test import BaseTest


class UserTest(BaseTest):
    def test_user_login(self):
        with app.app_context():
            response = self.app.post('/login', json={
                'username': 'test_user',
                'password': '123456'
            })
            token = response.json
            self.assertEqual(response.status_code, 200)  # Check if login is successful

            self.assertIn('access_token', token)

    def test_user_logout(self):
        with app.app_context():
            response = self.app.post('/login', json={
                'username': 'test_user',
                'password': '123456'
            })
            access_token = response.json['access_token']
            headers = {'Authorization': f'Bearer {access_token}'}
            response = self.app.post('/logout', headers=headers)
            self.assertEqual(response.status_code, 200)
