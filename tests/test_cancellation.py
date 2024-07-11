import unittest
from app import create_app, db
from app.models import User, Order, Product, OrderItem
from flask_jwt_extended import create_access_token

class CancellationTestCase(unittest.TestCase):
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

        self.product = Product(name='Test Product', description='Test Description', price=10.0, stock=100)
        db.session.add(self.product)
        db.session.commit()

        self.order = Order(user_id=self.user.id, status='Pending')
        db.session.add(self.order)
        db.session.commit()

        self.order_item = OrderItem(order_id=self.order.id, product_id=self.product.id, quantity=1)
        db.session.add(self.order_item)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_cancel_order(self):
        response = self.client.post(f'/api/v1/orders/{self.order.id}/cancel', headers=self.headers, json={
            'reason': 'Changed mind'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('order', response.json)
        self.assertEqual(response.json['order']['status'], 'Canceled')

if __name__ == '__main__':
    unittest.main()
