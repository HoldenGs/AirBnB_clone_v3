#!/usr/bin/python3

"""
Reviews Route
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_in_place(place_id=None):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews_for_place = [review.to_json() for review in place.reviews]
    return jsonify(reviews_for_place)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_get(review_id=None):
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_json())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id=None):
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_add(place_id=None):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    keys = data.keys()
    if 'user_id' not in keys:
        return 'Missing user_id', 400
    if storage.get('User', data['user_id']) is None:
        abort(404)
    if 'text' not in keys:
        return 'Missing text', 400
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_json()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_update(review_id=None):
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    try:
        data = request.get_json()
    except:
        return 'Not a JSON', 400
    if data is None:
        return 'Not a JSON', 400
    for k, v in data.items():
        if k not in ('id', 'created_at', 'updated_at', 'place_id', 'user_id',
                     'place_id'):
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_json())
