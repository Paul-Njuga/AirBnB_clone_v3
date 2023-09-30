#!/usr/bin/python3
"""View for Places objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_city_place(city_id):
    """Retrives list of all Place objects of a City"""
    places = storage.all(Place).values()
    places_list = []
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    for place in places:
        if place.to_dict()['city_id'] == city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list), 200


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_id(place_id):
    """Retrives Place object based on id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_id(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a new Place"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    rsp_dict = request.get_json()
    if not rsp_dict:
        abort(400, 'Not a JSON')
    if 'name' not in rsp_dict:
        abort(400, 'Missing name')
    if 'user_id' not in rsp_dict:
        abort(400, 'Missing user_id')
    user = storage.get('User', rsp_dict.get('user_id'))
    if not user:
        abort(404)

    # Create new place and save it
    rsp_dict['city_id'] = city_id
    new_place = Place(**rsp_dict)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates Place based on ID"""
    rsp_dict = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not rsp_dict:
        abort(400, 'Not a JSON')
    for key, value in rsp_dict.items():
        if key not in ['id', 'user_id', 'city_id',
                       'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
