from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.main.services import auth_service

def register_user():
    data = request.get_json()
    response, status = auth_service.register_user(data)
    return jsonify(response), status

def login_user():
    data = request.get_json()
    response, status = auth_service.login_user(data)
    return jsonify(response), status

@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    response, status = auth_service.get_profile(user_id)
    return jsonify(response), status
