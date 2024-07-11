from app.models import Order

def get_order_status(user_id, order_id):
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return None, 'Order not found'

    return order.status, None
