#!/usr/bin/python3
"""View for Amenity objects that handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """Retrives the list of all Amenity objects"""
    all_amenities = storage.all(Amenity).values()
    amenities_list = []

    # Append object dict to list
    for amenity in all_amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Retrives amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates a new amenity"""
    amenity = request.get_json()
    if not amenity:
        abort(400, 'Not a JSON')
    if 'name' not in amenity:
        abort(400, 'Missing name')

    # Create new amenity and save it
    new_amenity = Amenity(**amenity)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates amenity based on ID"""
    response = request.get_json()
    if not response:
        abort(400, 'Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    for key, value in response.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
