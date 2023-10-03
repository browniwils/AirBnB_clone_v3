#!/usr/bin/python3
"""HBNB RESTful api exposing various resource endpoints."""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/*": {"origins": ["*"]}})


@app.teardown_appcontext
def teardown(self):
    """Closes storage."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles not found resources."""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST")
    PORT = getenv("HBNB_API_PORT")

    if HOST is None:
        HOST = "0.0.0.0"
    if PORT is None:
        PORT = "5000"

    app.run(host=HOST, port=PORT,
            threaded=True)
