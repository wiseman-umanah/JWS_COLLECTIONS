#!/usr/bin/python3
"""Utility models like authorization"""
from flask_jwt_extended import get_jwt, get_jwt_identity
from functools import wraps
from flask import jsonify
from backend.models import storage
from backend.models.user import User

def role_required(role):
    """Checks user's role

    Args:
        role (str): the user's role (admin | user)
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get('sub').get('role') != role:
                return jsonify({'message': 'Access forbidden: insufficient privileges'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user():
    """gets the current user's details

    Returns:
        object: the user's object from database
    """
    user = get_jwt_identity()
    user_id = user.get('id')
    if user_id:
        return storage.get(User, user_id)
    return None
