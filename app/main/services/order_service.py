from app import db
from app.models import Order, OrderItem, Product

def create_order(user_id, items):
    order = Order(user_id=user_id, status='Pending')
    db.session.add(order)
    db.session.commit()

    total_price = 0
    for item in items:
        product = Product.query.get(item['product_id'])
        if not product or product.stock < item['quantity']:
            return None, 'Product not available or insufficient stock'

        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=product.price * item['quantity']
        )
        db.session.add(order_item)
        product.stock -= item['quantity']
        total_price += order_item.price

    db.session.commit()

    return order, total_price
