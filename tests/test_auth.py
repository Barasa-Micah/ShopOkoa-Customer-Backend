import unittest
from app import create_app, db
from app.models import User
from flask_jwt_extended import create_access_token

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password'
        }

        self.user = User(username='testuser', email='test@example.com', password_hash='password')
        db.session.add(self.user)
        db.session.commit()

        self.token = create_access_token(identity=self.user.id)
        self.headers = {
            'Authorization': f'Bearer {self.token}'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_register_user(self):
        response = self.client.post('/auth/register', json=self.user_data)
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        response = self.client.post('/auth/login', json=self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_get_profile(self):
        response = self.client.get('/auth/profile', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['email'], self.user.email)

if __name__ == '__main__':
    unittest.main()
