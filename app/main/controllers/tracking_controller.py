from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Order

@jwt_required()
def get_order_status(order_id):
    try:
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            return jsonify({'message': 'Order not found'}), 404

        return jsonify({'order_status': order.status}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500
