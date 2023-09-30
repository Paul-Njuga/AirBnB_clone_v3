#!/usr/bin/python3
"""View for User object that handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrives the list of all users"""
    all_users = storage.all(User).values()
    users_list = []

    # Append objects dict to list
    for user in all_users:
        users_list.append(user.to_dict())
    return jsonify(users_list), 200


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Retrives user by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a new user"""
    user = request.get_json()
    if not user:
        abort(400, 'Not a JSON')
    if 'email' not in user:
        abort(400, 'Missing email')
    if 'password' not in user:
        abort(400, 'Missing password')

    # Create new user and save
    new_user = User(**user)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates user based on ID"""
    response = request.get_json()
    if not response:
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    for key, value in response.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
