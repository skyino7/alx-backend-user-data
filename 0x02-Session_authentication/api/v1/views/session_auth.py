#!/usr/bin/env python3
"""
Session authentication
"""
from flask import Blueprint, jsonify, request, abort
import os
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login():
    """
    Login Method
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME', '_my_session_id'),
                        session_id)
    return response, 200


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    Logout Method
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
