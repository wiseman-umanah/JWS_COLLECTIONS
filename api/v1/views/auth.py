#!/usr/bin/python3
from api.v1.views import app_views
from backend.models.user import User
from backend.models import storage
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app_views.route('/login', methods=['POST'], strict_slashes=False)
def login_post():
    """Handles user login and issues JWT tokens."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = storage.get_user_by_email(email)

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity={'email': email, 'role': user.role})
    return jsonify({'token': access_token}), 200

@app_views.route('/signup', methods=['POST'], strict_slashes=False)
def signup_post():
    """Handles user registration."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    phoneNumber = data.get('phoneNumber')
    
    if storage.get_user_by_email(email=email):
        return jsonify({'message': 'Email address already exists'}), 400

    try:
        new_user = User(
            email=email, password=password,
            username=username, firstname=firstname,
            lastname=lastname, phoneNumber=phoneNumber
            )
        storage.new(new_user)
        storage.save()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app_views.route('/logout', methods=['POST'], strict_slashes=False)
@jwt_required()
def logout():
    """Handles user logout."""
    return jsonify({'message': 'User logged out'}), 200
