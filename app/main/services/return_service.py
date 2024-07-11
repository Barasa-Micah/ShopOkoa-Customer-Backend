from app import db
from app.models import Return, Order

def create_return(order_id, user_id, reason):
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order or order.status != 'Completed':
        return None, 'Order not eligible for return'

    return_request = Return(order_id=order_id, reason=reason, status='Pending')
    db.session.add(return_request)
    db.session.commit()

    return return_request, None
