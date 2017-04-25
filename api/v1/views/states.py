#!/usr/bin/python3

"""
States API
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/states', strict_slashes=False)
def states_list():
    states = storage.all('State').values()
    states_json = []
    for state in states:
        states_json.append(state.to_json())
    return jsonify(states_json)
