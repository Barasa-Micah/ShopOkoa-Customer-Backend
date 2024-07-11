from flask import Blueprint
from app.main.controllers import tracking_controller

bp = Blueprint('tracking', __name__)

bp.route('/orders/<int:order_id>/status', methods=['GET'])(tracking_controller.get_order_status)
