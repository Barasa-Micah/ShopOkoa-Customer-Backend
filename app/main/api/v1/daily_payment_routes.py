from flask import Blueprint
from app.main.controllers import daily_payment

bp = Blueprint('daily_payment', __name__)

# Route for handling STK push payment
bp.route('/daily_payment/stk_push/<string:user_id>', methods=['POST'])(daily_payment.stk_push_payment)

# Route for fetching payment history
bp.route('/daily_payment/history/<string:user_id>', methods=['GET'])(daily_payment.get_payment_history)

# Route for tracking daily payment status
bp.route('/daily_payment/track', methods=['GET'])(daily_payment.track_daily_payment)

# Route for paying for a missed day
bp.route('/daily_payment/pay_missed', methods=['POST'])(daily_payment.pay_for_missed_day)
