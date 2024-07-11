from app import db
from app.models import Payment, Order

def process_payment(order_id, user_id, amount):
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return None, 'Order not found'

    payment = Payment(order_id=order_id, amount=amount, status='Completed')
    db.session.add(payment)
    db.session.commit()

    return payment, None
