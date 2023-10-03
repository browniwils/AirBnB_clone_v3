#!/usr/bin/python3
"""HBNB RESTfull API endpoint for status and statistic."""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status():
    """Return status of API."""
    return jsonify(status="OK")


@app_views.route("/stats", strict_slashes=False)
def api_endpoint_stats():
    """Return API endpoints stats."""
    models = {
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
    }
    return jsonify({
        key.lower(): storage.count(value) for key, value in models.items()
        })
