from flask import Blueprint
from app.main.controllers import order_controller

bp = Blueprint('orders', __name__)

bp.route('/orders', methods=['POST'])(order_controller.create_order)
