from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Return, Order

@jwt_required()
def create_return(order_id):
    try:
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, user_id=user_id, status='Completed').first()
        if not order:
            return jsonify({'message': 'Order not eligible for return'}), 400

        data = request.get_json()
        reason = data.get('reason')
        if not reason:
            return jsonify({'message': 'Reason is required'}), 400

        return_request = Return(order_id=order_id, reason=reason, status='Pending')
        db.session.add(return_request)
        db.session.commit()

        return jsonify({'return': return_request.to_dict()}), 201

    except Exception as e:
        db.session.rollback() 
        return jsonify({'message': str(e)}), 500
