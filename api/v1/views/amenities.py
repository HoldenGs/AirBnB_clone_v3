#!/usr/bin/python3

"""
States Route
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_list():
    amenities = storage.all('Amenity').values()
    amenities_json = []
    for amenity in amenities:
        amenities_json.append(amenity.to_json())
    return jsonify(amenities_json)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_get(amenity_id=None):
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_json())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id=None):
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_add():
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'name' not in data.keys():
        return 'Missing name', 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_json()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_update(amenity_id=None):
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    try:
        data = request.get_json()
    except:
        return 'Not a JSON', 400
    if data is None:
        return 'Not a JSON', 400
    for k, v in data.items():
        if k not in ('id', 'created_at', 'updated_at'):
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_json())
