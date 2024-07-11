from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Payment, Order

@jwt_required()
def process_payment(order_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data or not data.get('amount'):
            return jsonify({'message': 'Invalid data'}), 400

        amount = data['amount']
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()

        if not order:
            return jsonify({'message': 'Order not found'}), 404

        if amount < order.amount:
            return jsonify({'message': f'Insufficient amount. Total amount due: {order.amount}'}), 400

        payment = Payment(
            order_id=order.id,
            amount=amount,
            status='Completed'
        )
        db.session.add(payment)
        order.status = 'Completed'
        db.session.commit()

        return jsonify({'message': 'Payment successful', 'order': order.to_dict(), 'payment': payment.to_dict()}), 201

    except Exception as e:
        db.session.rollback()  # Rollback changes in case of error
        return jsonify({'message': str(e)}), 500