from flask import Blueprint
from app.main.controllers import cancellation_controller

bp = Blueprint('cancellation', __name__)

bp.route('/orders/<int:order_id>/cancel', methods=['POST'])(cancellation_controller.cancel_order)
