#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrive the list of all State objects"""
    all_states = storage.all(State).values()
    states_list = []

    # Append object dict to list
    for state in all_states:
        states_list.append(state.to_dict())
    return jsonify(states_list), 200


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_by_id(state_id):
    """Retrives a state by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a new state"""
    state = request.get_json()
    if not state:
        abort(400, 'Not a JSON')
    if 'name' not in state:
        abort(400, 'Missing name')

    # Create new state and save it
    new_state = State(**state)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates state based on ID"""
    response = request.get_json()
    if not response:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for key, value in response.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
