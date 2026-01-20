# app/utils/helpers.py
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify
import re

# --------------------------
# Admin-only route decorator
# --------------------------
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if identity['user_type'] != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

# --------------------------
# Validate Email
# --------------------------
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
