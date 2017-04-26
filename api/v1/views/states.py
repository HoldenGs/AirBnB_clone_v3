#!/usr/bin/python3

"""
States API
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_list():
    states = storage.all('State').values()
    states_json = []
    for state in states:
        states_json.append(state.to_json())
    return jsonify(states_json)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_get(state_id=None):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_json())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def state_delete(state_id=None):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_add():
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'name' not in data.keys():
        return 'Missing name', 400
    state = State(**data)
    state.save()
    return jsonify(state.to_json()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_update(state_id=None):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    try:
        data = request.get_json()
    except:
        return 'Not a JSON', 400
    if data is None:
        return 'Not a JSON', 400
    for k, v in data.items():
        if k not in ('id', 'created_at', 'updated_at'):
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_json())
