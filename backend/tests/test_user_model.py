import unittest
import datetime

from main import db
from main.models.user import User
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

    def test_add_user(self):
        new_user = self.createUser()
        self.assertTrue(new_user == User.query.filter_by(username='tester').first())

    def test_check_password(self):
        new_user = self.createUser()
        self.assertTrue(new_user.check_password('12345'))
        self.assertFalse(new_user.check_password('123456'))

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

    def test_logout_success(self):
        new_user = self.createUser()

        with app.test_client() as client:
            response = client.post(
                '/alifs/api/auth/login',
                json={'username': 'tester', 'password': '12345'}
            )

            response_logout = client.get('/alifs/api/auth/logout')
            response_data = response_logout.get_json()

            self.assertTrue('logged_in' not in session)
            self.assertIn('Successfully logged out', response_data['message'])


if __name__ == '__main__':
    unittest.main()
