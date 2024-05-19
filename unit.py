import unittest
from flask import url_for
from app import create_app, db
from app.config import TestConfig

class BasicViewTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_page(self):
        response = self.client.get(url_for('user.login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login - Study Perth Assistant', response.data)
        self.assertIn(b'Log in', response.data)

    def test_register_page(self):
        response = self.client.get(url_for('user.register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Account - Study Perth Assistant', response.data)
        self.assertIn(b'Sign up', response.data)

    def test_profile_page(self):
        # This test assumes there is a profile route and a user must be logged in
        with self.client:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'User Information', response.data)
            self.assertIn(b'Answered Questions', response.data)

    def test_post_question_page(self):
        # This test assumes the user must be logged in to post a question
        with self.client:
            response = self.client.get(url_for('question.post'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Post a New Question', response.data)
            self.assertIn(b'Enter title (up to 50 characters)', response.data)

    def test_answer_question_page(self):
        # This test assumes there is an 'answered questions' route
        with self.client:
            response = self.client.get(url_for('question.answered'))  
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Answered Questions', response.data)
            self.assertIn(b'What are the best places to visit in Perth?', response.data)

if __name__ == '__main__':
    unittest.main()
