#!/usr/bin/python3

"""
Flask app
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {'origins': "0.0.0.0"}})


@app.errorhandler(404)
def handle_404(exception):
    error = {"error": "Not found"}
    return jsonify(error), 404


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'))
