#!/usr/bin/python3

from flask_jwt_extended import jwt_required
from api.v1.views import app_views
from api.v1.utils.authorization import role_required
from backend.models import storage
from backend.models.user import User
from flask import jsonify, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required('admin')
def users():
    list_users = []
    users = storage.all(User).values()
    if not users:
        return jsonify({'message': 'No user was created'}), 404
    for user in users:
        list_users.append(user.to_dict())
    return jsonify(list_users), 200

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user_profile(user_id):
    user = storage.get(User, user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_user_profile(user_id):
    data = request.get_json()
    user = storage.get(User, user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Update user fields
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    storage.save()
    return jsonify(user.to_dict()), 200

