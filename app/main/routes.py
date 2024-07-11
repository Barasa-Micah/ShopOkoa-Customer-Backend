from flask import Blueprint

bp = Blueprint('main', __name__)

from .api.v1 import auth_routes, order_routes, tracking_routes, payment_routes, cancellation_routes, return_routes

bp.register_blueprint(auth_routes.bp, url_prefix='/api/v1')
bp.register_blueprint(order_routes.bp, url_prefix='/api/v1')
bp.register_blueprint(tracking_routes.bp, url_prefix='/api/v1')
bp.register_blueprint(payment_routes.bp, url_prefix='/api/v1')
bp.register_blueprint(cancellation_routes.bp, url_prefix='/api/v1')
bp.register_blueprint(return_routes.bp, url_prefix='/api/v1')
