#!/usr/bin/python3

"""
Places Route
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_list(city_id=None):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places_in_city = [place.to_json() for place in city.places]
    return jsonify(places_in_city)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_get(place_id=None):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_json())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id=None):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_add(city_id=None):
    city = storage.get('City', city_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    keys = data.keys()
    if 'user_id' not in keys:
        return 'Missing user_id', 400
    if storage.get('User', user_id) is None:
        abort(404)
    if 'name' not in keys:
        return 'Missing name', 400
    place = Place(**data)
    place.save()
    return jsonify(place.to_json()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_update(place_id=None):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    try:
        data = request.get_json()
    except:
        return 'Not a JSON', 400
    if data is None:
        return 'Not a JSON', 400
    for k, v in data.items():
        if k not in ('id', 'created_at', 'updated_at', 'user_id', 'city_id'):
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_json())
