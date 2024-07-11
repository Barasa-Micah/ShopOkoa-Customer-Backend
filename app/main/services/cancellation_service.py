from app import db
from app.models import Order, Product, OrderItem

def cancel_order(order_id, user_id):
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order or order.status != 'Pending':
        return None, 'Order cannot be canceled'

    for item in order.items:
        product = Product.query.get(item.product_id)
        if product:
            product.stock += item.quantity

    order.status = 'Canceled'
    db.session.commit()

    return order, None