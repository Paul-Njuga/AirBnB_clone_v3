#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_state_cities(state_id):
    """Retrives list of all City objects in a State"""
    cities = storage.all(City).values()
    cities_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in cities:
            if city.to_dict()['state_id'] == state_id:
                cities_list.append(city.to_dict())
    return jsonify(cities_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_id(city_id):
    """Retrives City object based on id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_id(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a new city"""
    rsp_dict = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not rsp_dict:
        abort(400, 'Not a JSON')
    if 'name' not in rsp_dict:
        abort(400, 'Missing name')

    # Create new state and save it
    rsp_dict['state_id'] = state_id
    new_city = State(**rsp_dict)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates city based on ID"""
    rsp_dict = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not rsp_dict:
        abort(400, 'Not a JSON')
    for key, value in rsp_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
