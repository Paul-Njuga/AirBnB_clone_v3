#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrive the list of all State objects"""
    all_states = storage.all(State).values()
    states_list = []

    # Append object dict to list
    for state in all_states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_by_id(state_id):
    """Retrives a state by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def delete_state(state_id):
    """Deletes a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({})


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a new state"""
    state = request.get_json()
    if not request.json:
        abort(404, 'Not a JSON')
    if 'name' not in request.json:
        abort(404, 'Missing name')

    # Create new state and save it
    new_state = State(**state)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201
