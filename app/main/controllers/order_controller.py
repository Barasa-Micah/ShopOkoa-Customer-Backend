from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Order, OrderItem, Product, User

@jwt_required()
def create_order():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data or not data.get('items'):
            return jsonify({'message': 'Invalid data'}), 400

        order = Order(user_id=user_id, status='Pending')
        db.session.add(order)
        db.session.commit()

        total_price = 0
        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if not product or product.stock < item['quantity']:
                return jsonify({'message': 'Product not available or insufficient stock'}), 400

            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=product.price * item['quantity']
            )
            db.session.add(order_item)
            product.stock -= item['quantity']
            total_price += order_item.price  # Accumulate order item price to total_price

        # Update the order's total_price attribute and amount column
        order.total_price = total_price
        order.amount = total_price  # Set the amount column to the total_price
        db.session.commit()

        return jsonify({'order': order.to_dict(), 'total_price': total_price}), 201

    except Exception as e:
        db.session.rollback()  # Rollback changes in case of error
        return jsonify({'message': str(e)}), 500