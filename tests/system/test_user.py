from models.user import UserModel
from tests.base_test import BaseTest
from flask.testing import FlaskClient
import json

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app as client:
            with self.app_context():
                # this test is pretending to be our client of API, as if we were an external user
                response = client.post('/register', data={'username': 'test', 'password': 'abcd'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully'}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app as client:
            with self.app_context():
                # this test is pretending to be our client of API, as if we were an external user
                client.post('/register', data={'username': 'test', 'password': 'abcd'})
                auth_response = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': 'abcd'}),
                                           headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_response.data).keys()) # ['access_token]


    def test_register_duplicate_user(self):
        #  we just need to run the previous request once again

        with self.app as client:
            with self.app_context():
                # this test is pretending to be our client of API, as if we were an external user
                client.post('/register', data={'username': 'test', 'password': 'abcd'})
                response = client.post('/register', data={'username': 'test', 'password': 'abcd'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists.'},
                                     json.loads(response.data))
