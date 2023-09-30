#!/usr/bin/python3
"""View for Review objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_review(place_id):
    """Retrives list of all Review objects of a Place"""
    reviews = storage.all(Review).values()
    reviews_list = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    for review in reviews:
        if review.to_dict()['place_id'] == place_id:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list), 200


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_id(review_id):
    """Retrives Review object based on id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review_id(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a new Review"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    rsp_dict = request.get_json()
    if not rsp_dict:
        abort(400, 'Not a JSON')
    if 'text' not in rsp_dict:
        abort(400, 'Missing text')
    if 'user_id' not in rsp_dict:
        abort(400, 'Missing user_id')
    user = storage.get('User', rsp_dict.get('user_id'))
    if not user:
        abort(404)

    # Create new place and save it
    rsp_dict['place_id'] = place_id
    new_review = Review(**rsp_dict)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates Review based on ID"""
    rsp_dict = request.get_json()
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not rsp_dict:
        abort(400, 'Not a JSON')
    for key, value in rsp_dict.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
