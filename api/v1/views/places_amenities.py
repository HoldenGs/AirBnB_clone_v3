#!/usr/bin/python3

"""
Place Amenities Route
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Amenity, Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_at_place(place_id=None):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenities = [amenity.to_json() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_at_place(place_id=None, amenity_id=None):
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if place is None or amenity is None or amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_amenity_to_place(place_id=None, amenity_id=None):
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_json()), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_json()), 201
