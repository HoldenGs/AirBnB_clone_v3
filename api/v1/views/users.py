#!/usr/bin/python3

"""
Users Route
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_list():
    users = storage.all('User').values()
    users_json = []
    for user in users:
        users_json.append(user.to_json())
    return jsonify(users_json)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_get(user_id=None):
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id=None):
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_add():
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    keys = data.keys()
    if 'email' not in keys:
        return 'Missing email', 400
    elif 'password' not in keys:
        return 'Missing password', 400
    user = User(**data)
    state.save()
    return jsonify(user.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_update(user_id=None):
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    try:
        data = request.get_json()
    except:
        return 'Not a JSON', 400
    if data is None:
        return 'Not a JSON', 400
    for k, v in data.items():
        if k not in ('id', 'created_at', 'updated_at', 'email'):
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_json())
