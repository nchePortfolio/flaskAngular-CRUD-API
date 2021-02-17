import unittest
import datetime
import time

from main import db
from main.models.user import User
from main.models.token import BlacklistToken
from tests.base import BaseTestCase, app
from flask import session


class TestUserModel(BaseTestCase):

    def createUser(self):
        new_user = User(
            email='email@test.fr',
            username='tester',
            password='12345',
            admin=True,
            registered_on=datetime.datetime.utcnow()
       )
        db.session.add(new_user)
        db.session.commit()

        return new_user

    def register_user(self, client):
        response = client.post(
            '/alifs/api/auth/register',
            json={'username': 'tester', 'email': 'email@test.fr','password': '12345'}
        )
        return response


    def test_registration(self):
        """ Test for user registration """
        with app.test_client() as client:
            response = self.register_user(client)

            data = response.get_json()

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    
    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        user = self.createUser()
        with app.test_client() as client:
            response = self.register_user(client)

            data = response.get_json()

            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)


    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with app.test_client() as client:
            # register user
            response_register = self.register_user(client)

            # login registered user 
            response_login = client.post(
                '/alifs/api/auth/login',
                json={'username': 'tester', 'password': '12345'}
            )

            data = response_login.get_json()

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response_login.content_type == 'application/json')
            self.assertEqual(response_login.status_code, 200)


    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with app.test_client() as client:
            # login non registered user 
            response = client.post(
                '/alifs/api/auth/login',
                json={'username': 'tester', 'password': '12345'}
            )

            data = response.get_json()

            self.assertTrue(data['status'] == 'fail')
            self.assertIn('does not exist', data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

        
    def test_user_status(self):
        """ Test for user status """
        # register user
        with app.test_client() as client:
            response_register = self.register_user(client)
            data_register = response_register.get_json()

            # get user status
            response = client.get(
                    '/alifs/api/auth/status',
                    headers=dict(Authorization='Bearer ' + data_register['auth_token'])
                )

            data = response.get_json()

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == 'email@test.fr')
            self.assertIn(data['data']['admin'], [True, False])
            self.assertEqual(response.status_code, 200)


    def test_login_success(self):
        new_user = self.createUser()

        with app.test_client() as client:
            response = client.post(
                '/alifs/api/auth/login',
                json={'username': 'tester', 'password': '12345'}
            )

            response_data = response.get_json()
            self.assertEqual(response_data['status'], 'success')
            self.assertEqual(session['logged_in'], True)
            self.assertEqual(session['username'], 'tester')


    def test_login_failure_wrong_password(self):
        new_user = self.createUser()

        with app.test_client() as client:
            response = client.post(
                '/alifs/api/auth/login',
                json={'username': 'tester', 'password': 'abcde'}
            )

            response_data = response.get_json()
            self.assertEqual(response_data['status'], 'fail')
            self.assertIn('incorrect password', response_data['message'])
            self.assertTrue('logged_in' not in session)


    def test_login_failure_wrong_username(self):
        new_user = self.createUser()

        with app.test_client() as client:
            response = client.post(
                '/alifs/api/auth/login',
                json={'username': 'notatester', 'password': '12345'}
            )

            response_data = response.get_json()
            self.assertEqual(response_data['status'], 'fail')
            self.assertIn('notatester does not exist', response_data['message'])
            self.assertTrue('logged_in' not in session)


    def test_valid_logout(self):
        """ Test for logout before token expires """
        with app.test_client() as client:
            # register user
            response_register = self.register_user(client)

            # login registered user 
            response_login = client.post(
                '/alifs/api/auth/login',
                json={'username': 'tester', 'password': '12345'}
            )
            data = response_login.get_json()
            
            # valid token logout
            response = self.client.get(
                    '/alifs/api/auth/logout',
                    headers=dict(Authorization='Bearer ' + data['auth_token'])
                    )
            data = response.get_json()

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)


    def test_invalid_logout(self):
        """ Test for logout after token expires """
        with app.test_client() as client:
            # register user
            response_register = self.register_user(client)

            # login registered user 
            response_login = client.post(
                '/alifs/api/auth/login',
                json={'username': 'tester', 'password': '12345'}
            )
            data = response_login.get_json()
            
            # logout after token expired
            time.sleep(3)
            response = self.client.get(
                    '/alifs/api/auth/logout',
                    headers=dict(Authorization='Bearer ' + data['auth_token'])
                    )
            data = response.get_json()
        
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)


    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a valid token gets blacklisted """
        with app.test_client() as client:
            # register user
            response_register = self.register_user(client)

            # login registered user 
            response_login = client.post(
                '/alifs/api/auth/login',
                json={'username': 'tester', 'password': '12345'}
            )
            data = response_login.get_json()

            # blacklist a valid token
            blacklist_token = BlacklistToken(token=data['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()

            # blacklisted valid token logout
            response = self.client.get(
                    '/alifs/api/auth/logout',
                    headers=dict(Authorization='Bearer ' + data['auth_token'])
                    )

            data = response.get_json()
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)


    def test_valid_blacklisted_token_user_status(self):
        """ Test for logout after a valid token gets blacklisted """
        with app.test_client() as client:
            # register user
            response_register = self.register_user(client)

            data = response_register.get_json()

            # blacklist a valid token
            blacklist_token = BlacklistToken(token=data['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()

            # get user status
            response = client.get(
                    '/alifs/api/auth/status',
                    headers=dict(Authorization='Bearer ' + data['auth_token'])
                )

            data = response.get_json()

            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)


    # def test_user_status_malformed_bearer_token(self):
    #     """ Test for user status with malformed bearer token"""
    #     with app.test_client() as client:
    #         # register user
    #         response_register = self.register_user(client)

    #         data = response_register.get_json()

    #         # get user status
    #         response = client.get(
    #                 '/alifs/api/auth/status',
    #                 headers=dict(Authorization='Bearer' + data['auth_token'])
    #             )

    #         data = response.get_json()
    #         # print(data)

    #         self.assertTrue(data['status'] == 'fail')
    #         self.assertTrue(data['message'] == 'Bearer token malformed.')
    #         self.assertEqual(response.status_code, 401)



if __name__ == '__main__':
    unittest.main()
