from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

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
