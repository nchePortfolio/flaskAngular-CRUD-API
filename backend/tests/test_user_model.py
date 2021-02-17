import unittest
import datetime
import time

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


    def test_encode_auth_token(self):
        user = self.createUser()
        auth_token = user.encode_auth_token(user.id)

        self.assertTrue(isinstance(auth_token, str))
        self.assertEqual(len(auth_token.split('.')), 3)
        self.assertTrue(User.decode_auth_token(auth_token == 1))

    def test_decode_auth_token_valid(self):
        user = self.createUser()
        auth_token = user.encode_auth_token(user.id)

        self.assertTrue(User.decode_auth_token(auth_token) == user.id)


    def test_decode_auth_token_expired(self):
        user = self.createUser()
        auth_token = user.encode_auth_token(user.id)
        time.sleep(3)

        self.assertIn('Signature expired', User.decode_auth_token(auth_token))


    def test_decode_auth_token_invalid(self):
        user = self.createUser()
        auth_token = user.encode_auth_token(user.id)

        self.assertIn('Invalid token', User.decode_auth_token('bla.bla.bla'))     


if __name__ == '__main__':
    unittest.main()
