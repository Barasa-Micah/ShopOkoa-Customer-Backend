import unittest
from app import create_app, db
from app.models import User, Order
from flask_jwt_extended import create_access_token

class TrackingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.user = User(username='testuser', email='test@example.com', password='password')
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

    def test_get_order_status(self):
        order = Order(user_id=self.user.id, status='Pending')
        db.session.add(order)
        db.session.commit()

        response = self.client.get(f'/api/v1/orders/{order.id}/status', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('order_status', response.json)

if __name__ == '__main__':
    unittest.main()
