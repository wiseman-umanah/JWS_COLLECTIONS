#!/usr/bin/python3
"""Route handling for users"""
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
    """Retrieves all Users restricted to admin

    Returns:
        json (list): list of all users
    """
    list_users = []
    users = storage.all(User).values()
    if not users:
        return jsonify({'message': 'No user was created'}), 404
    list_users = [user.from_dict() for user in users]
    return jsonify(list_users), 200


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user_profile(user_id):
    """Get user based on id

    Args:
        user_id (str): id of the user

    Returns:
        json (dict): dictionary repr of the User
    """
    user = storage.get(User, user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.from_dict()), 200


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_user_profile(user_id):
    """updates a user object, based on id

    Args:
        user_id (str): id of the user

    Returns:
        json (dict): dictionary repr of the User
    """
    data = request.get_json()

    user = storage.get(User, user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Update user fields
    for key, value in data.items():
        if hasattr(user, key) and key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.from_dict()), 200

