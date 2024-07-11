from flask import Blueprint
from app.main.controllers import auth_controller

bp = Blueprint('auth', __name__)

bp.route('/auth/register', methods=['POST'])(auth_controller.register_user)
bp.route('/auth/login', methods=['POST'])(auth_controller.login_user)
bp.route('/auth/profile', methods=['GET'])(auth_controller.get_profile)
