from sqlalchemy.exc import SQLAlchemyError
from models import DailyPaymentModel, PaymentHistoryModel
from models import UserModel
from utils import send_stk_push
from app import db

def process_stk_push_payment(user_id, amount=100, date=None):
    try:
        # Fetch the user from the database
        user = UserModel.query.get_or_404(user_id)

        # Check if user has a phone number
        if not hasattr(user, 'phone_number'):
            return None, "User does not have a phone number"

        # Send the STK Push
        success = send_stk_push(user.phone_number, amount)
        if success:
            # Mark payment as paid in the DailyPaymentModel
            DailyPaymentModel.mark_paid(user.id, date)
            return "STK push successful, payment marked as paid.", None
        else:
            return None, "STK push failed"

    except SQLAlchemyError as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}"
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

def fetch_payment_history(user_id):
    try:
        # Query payment history for the given user
        payment_history = PaymentHistoryModel.query.filter_by(user_id=user_id).all()
        return payment_history, None
    except SQLAlchemyError as e:
        return None, f"Database error: {str(e)}"
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"
