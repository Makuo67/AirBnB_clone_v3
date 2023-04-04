#!/usr/bin/python3
"""Users api"""

from flask import Blueprint, jsonify, request, abort
from app.models import User

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')


@users_bp.route('/', methods=['GET'])
def get_users():
    """Get users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user id"""
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@users_bp.route('/', methods=['POST'])
def create_user():
    """create user"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user = User(email=data['email'], password=data['password'])
    user.save()
    return jsonify(user.to_dict()), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """delete user"""
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    user.delete()
    return jsonify({}), 200
