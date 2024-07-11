from flask import Blueprint
from app.main.controllers import return_controller

bp = Blueprint('returns', __name__)

bp.route('/orders/<int:order_id>/return', methods=['POST'])(return_controller.create_return)
