#!/usr/bin/env python3

import unittest
from config_test import app, db
from models.user import User

# Import the test configuration
app.config.from_pyfile('config_test.py')


class UserTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        with app.app_context():
            user = User(
                email="test@eailcom",
                username="tesing",
                password="test",
                first_name="Test",
                last_name="User",
                verification_code="23bbdh"
            )
            user.save()
            rt_user = User.get(user.id)
            self.assertEqual(user, rt_user)
            self.assertEqual(user.id, rt_user.id)
            self.assertEqual(user.email, rt_user.email)
            self.assertEqual(user.username, rt_user.username)
            self.assertEqual(user.password, rt_user.password)
            self.assertEqual(user.first_name, rt_user.first_name)
            self.assertEqual(user.verification_code, rt_user.verification_code)

    def test_user_deletion(self):
        """Try Access a deleted user"""
        with app.app_context():
            user = User(
                email="test@eailcom",
                username="tesing",
                password="test",
                first_name="Test",
                last_name="User",
                verification_code="23bbdh"
            )
            user.save()
            user.delete()
            rt_user = User.get(user.id)
            self.assertIsNone(rt_user)

if __name__ == '__main__':
    unittest.main()
