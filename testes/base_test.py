import json
from unittest import TestCase
from app import app
from db import db
from models.user import UserModel


class BaseTest(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

            # Create test user for authentication
            user = UserModel(username='test_user', password='123456')
            user.save_to_db()

        # Authenticate the test user
        response = self.app.post('/login', json={
            'username': 'test_user',
            'password': '123456'
        })
        self.token = response.json['access_token']

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def get_auth_token(self, username, password):
        # Simulate generating JWT token for authentication
        response = self.app.post('/login', json={'username': username, 'password': password})
        auth_token = json.loads(response.data)['access_token']
        user_id = json.loads(response.data)['user_id']
        return auth_token, user_id
