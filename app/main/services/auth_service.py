from flask_jwt_extended import create_access_token, create_refresh_token
from app import db
from app.models import User
from app.schemas import UserSchema, UserCreationSchema, UserUpdateSchema
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(email=email).first():
        return {'message': 'Email already registered'}, 400
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    user_schema = UserSchema()
    return user_schema.dump(new_user), 201

def login_user(data):
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return {'message': 'Invalid credentials'}, 401
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': UserSchema().dump(user)
    }, 200

def get_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found'}, 404

    return UserSchema().dump(user), 200
