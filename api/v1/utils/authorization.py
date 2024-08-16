from flask_jwt_extended import get_jwt, get_jwt_identity
from functools import wraps
from flask import jsonify
from backend.models import storage
from backend.models.user import User

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') != role:
                return jsonify({'message': 'Access forbidden: insufficient privileges'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user():
    user_id = get_jwt_identity()
    if user_id:
        return storage.get(User, user_id)
    return None
