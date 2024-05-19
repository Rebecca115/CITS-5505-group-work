import pdb
import unittest
from flask import current_app
from run import create_app
from models import db, User, Question

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('app.conf.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register_user(self, username, email, password):
        return self.client.post('/user/register', data={
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': password
        }, follow_redirects=True)

    def login_user(self, email, password):
        return self.client.post('/user/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_register(self):
        response = self.register_user('testuser', 'testuser@example.com', 'testpassword')
        self.assertEqual(response.status_code, 200)
        # pdb.set_trace()
        user = User.query.filter_by(email='testuser@example.com').first()
        self.assertIsNotNone(user)

    def test_login(self):
        self.register_user('testuser', 'testuser@example.com', 'testpassword')
        response = self.login_user('testuser@example.com', 'testpassword')
        self.assertEqual(response.status_code, 200)  # Should be redirected to home page after login

    def test_create_question(self):
        self.register_user('testuser', 'testuser@example.com', 'testpassword')


        user = User.query.filter_by(username='testuser').first()
        user.email_verified = True
        db.session.commit()

        self.login_user('testuser', 'testpassword')

        response = self.client.post('/post', data={
            'title': 'Test Question111111',
            'content': 'This is a test question111111',
            'category': 'Test11111'
        }, follow_redirects=True)


        page = response.data.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        question = Question.query.filter_by(title='Test Question111111').first()
        print(question)
        pdb.set_trace()
        self.assertIsNotNone(question)
        self.assertEqual(question.content, 'This is a test question')

    def test_browse_questions(self):
        self.register_user('testuser', 'testuser@example.com', 'testpassword')
        self.login_user('testuser@example.com', 'testpassword')

        user = User.query.filter_by(email='testuser@example.com').first()
        question1 = Question(title='Test Question 1', content='Content for test question 1', user_id=user.id, category='Test')
        question2 = Question(title='Test Question 2', content='Content for test question 2', user_id=user.id, category='Test')
        db.session.add_all([question1, question2])
        db.session.commit()

        response = self.client.get('/browse')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Question 1', response.data)
        self.assertIn(b'Test Question 2', response.data)

    def test_question_detail(self):
        self.register_user('testuser', 'testuser@example.com', 'testpassword')
        self.login_user('testuser@example.com', 'testpassword')

        user = User.query.filter_by(email='testuser@example.com').first()
        question = Question(title='Test Question Detail', content='Content for test question detail', user_id=user.id, category='Test')
        db.session.add(question)
        db.session.commit()

        response = self.client.get(f'/question/{question.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Question Detail', response.data)
        self.assertIn(b'Content for test question detail', response.data)

if __name__ == '__main__':
    unittest.main()
