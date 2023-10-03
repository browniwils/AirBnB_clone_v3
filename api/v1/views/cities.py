#!/usr/bin/python3
"""Module for views API cities endpoints."""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def cities(state_id):
    """Retrieve all state objects."""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    return jsonify([city.to_dict() for city in state_obj.cities])


@app_views.route("/cities/<city_id>", strict_slashes=False)
def cities_id(city_id):
    """Retrieve city object."""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"], strict_slashes=False)
def city_id_del(city_id):
    """Deletes city object."""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def city_add(state_id):
    """Add city."""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if "name" not in body.keys():
        abort(400, "Missing name")
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    new_city = City(**body)
    new_city.state_id = state_obj.id
    new_city.save()
    return jsonify(new_city.to_dict()), "201"


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def city_update(city_id):
    """Updates city object."""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "created_at", "update_at"]:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict())
