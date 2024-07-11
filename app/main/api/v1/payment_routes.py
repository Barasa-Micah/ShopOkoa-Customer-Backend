from flask import Blueprint
from app.main.controllers import payment_controller

bp = Blueprint('payment', __name__)

bp.route('/orders/<int:order_id>/payment', methods=['POST'])(payment_controller.process_payment)
