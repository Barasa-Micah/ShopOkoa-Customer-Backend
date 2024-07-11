import unittest
from app import create_app, db
from app.models import User, Order, Product, OrderItem, Return
from flask_jwt_extended import create_access_token

class ReturnTestCase(unittest.TestCase):
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

        self.order = Order(user_id=self.user.id, status='Completed')
        db.session.add(self.order)
        db.session.commit()

        self.order_item = OrderItem(order_id=self.order.id, product_id=self.product.id, quantity=1)
        db.session.add(self.order_item)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_return(self):
        response = self.client.post(f'/api/v1/orders/{self.order.id}/return', headers=self.headers, json={
            'reason': 'Defective product'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('return', response.json)

    def test_get_returns(self):
        return_obj = Return(order_id=self.order.id, reason='Defective product')
        db.session.add(return_obj)
        db.session.commit()

        response = self.client.get('/api/v1/returns', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('returns', response.json)

if __name__ == '__main__':
    unittest.main()
