from datetime import datetime
import logging
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from app.models import DailyPaymentModel, PaymentHistoryModel
from app.models import User
from app.utils import send_stk_push
from app import db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@jwt_required()
def stk_push_payment(user_id):
    try:
        # Log the incoming request data
        data = request.get_json()
        logger.debug(f"Received data: {data}")

        # Ensure the amount is retrieved from the request or set default
        amount = data.get('amount', 100)
        date_str = data.get('date', None)
        phone_number = data.get('phone_number', None)  # Get phone number from the request
        logger.debug(f"Using amount: {amount}, date: {date_str}, phone number: {phone_number}")

        # Fetch the user from the database
        user = User.query.get_or_404(user_id)
        
        # Use the phone number from the request or fetch from the database
        if phone_number is None:
            if hasattr(user, 'phone_number'):
                phone_number = user.phone_number
            else:
                logger.error("User does not have a phone number")
                return jsonify({"error": "User does not have a phone number"}), 400
        
        logger.debug(f"Using phone number: {phone_number}")

        # Convert date string to a date object
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert string to date
        else:
            date = None  # Handle case where date is not provided

        # Send the STK Push
        success = send_stk_push(phone_number, amount)
        logger.debug(f"STK push success status: {success}")

        if success:
            DailyPaymentModel.mark_paid(user.id, date)
            logger.info(f"Payment marked as paid for user: {user_id} on {date}")
            return jsonify({"message": "STK push successful, payment marked as paid."}), 200
        else:
            logger.error("STK push failed")
            return jsonify({"error": "STK push failed"}), 500

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database error occurred."}), 500
    except Exception as e:
        logger.exception("An unexpected error occurred")
        return jsonify({"error": str(e)}), 500

@jwt_required()
def get_payment_history(user_id):
    try:
        payment_history = PaymentHistoryModel.query.filter_by(user_id=user_id).all()
        return jsonify([payment.to_dict() for payment in payment_history]), 200

    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database error occurred."}), 500
    except Exception as e:
        logger.exception("An unexpected error occurred")
        return jsonify({"error": str(e)}), 500

@jwt_required()
def track_daily_payment():
    user_id = get_jwt_identity()
    date = datetime.utcnow().date()  # Use today's date by default

    # Check if the user has already marked a payment for today
    payment = DailyPaymentModel.query.filter_by(user_id=user_id, date=date).first()

    if payment:
        if payment.paid:
            return jsonify({"message": "Payment already marked as paid for today."}), 200
        else:
            return jsonify({"message": "Payment not marked for today."}), 200
    else:
        # If no payment record exists, it is considered unpaid (not marked)
        DailyPaymentModel.mark_as_unpaid(user_id, date)
        return jsonify({"message": "No payment record for today. Marked as unpaid."}), 200

# Function to pay for a missed day
@jwt_required()
def pay_for_missed_day():
    data = request.get_json()
    date_str = data.get('date')  # Date of the missed payment
    amount = data.get('amount', 100)  # Optional amount, default to 100
    phone_number = data.get('phone_number')  # Get phone number from request data

    if date_str is None:
        return jsonify({"error": "Date is required."}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert to date
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    user_id = get_jwt_identity()  # Get the current user's ID
    user = User.query.get_or_404(user_id)

    # If phone number is not provided, use the user's phone number
    if phone_number is None:
        phone_number = user.phone_number

    # Send the STK Push payment
    success = send_stk_push(phone_number, amount)

    if success:
        DailyPaymentModel.mark_paid(user.id, date)  # Mark as paid
        return jsonify({"message": "Payment for missed day successfully processed."}), 200
    else:
        return jsonify({"error": "Payment failed."}), 500