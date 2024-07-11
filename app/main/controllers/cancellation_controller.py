from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Order, Product, OrderItem

@jwt_required()
def cancel_order(order_id):
    try:
        user_id = get_jwt_identity()
        
        # Ensure the order exists and is cancellable by the authenticated user
        order = Order.query.filter_by(id=order_id, user_id=user_id, status='Pending').first()
        if not order:
            return jsonify({'message': 'Order not found or cannot be canceled'}), 404

        # Release reserved stock for each item in the order
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity

        # Update order status to 'Canceled' and commit changes
        order.status = 'Canceled'
        db.session.commit()

        return jsonify({'message': 'Order canceled successfully'}), 200

    except Exception as e:
        db.session.rollback()  # Rollback changes if an error occurs
        return jsonify({'message': str(e)}), 500