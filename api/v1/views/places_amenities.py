#!/usr/bin/python3
"""View for Amenities objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
import models
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenitie(place_id):
    """Retrives list of all Amenity objects of a Place"""
    amenities = storage.all(Amenity).values()
    amenities_list = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if models.storage_t == 'db':
        for amenity in place.amenities:
            amenities_list.append(amenity.to_dict())
    else:
        amenities_list = place.amenities
    return jsonify(amenities_list), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity_id(place_id, amenity_id):
    """Deletes a Amenity object"""
    place = storage.get('Place', place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if models.storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
    if models.storage_t == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity.id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def create_place_amenity(place_id, amenity_id):
    """Creates a new Amenity"""
    place = storage.get('Place', place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if models.storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
    else:
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
    if models.storage_t == 'db':
        place.amenities.add(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
