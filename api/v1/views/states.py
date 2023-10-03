#!/usr/bin/python3
"""Module for views API states endpoints."""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def states():
    """Retrieve all state objects."""
    state_objs = storage.all(State)
    return jsonify([state.to_dict() for state in state_objs.values()])


@app_views.route("/states/<state_id>", strict_slashes=False)
def states_id(state_id):
    """Retrieve state object."""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    return jsonify(state_obj.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def state_id_del(state_id):
    """Deletes state object."""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    state_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_add():
    """Add a state."""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if "name" not in body.keys():
        abort(400, "Missing name")

    new_state = State(**body)
    new_state.save()
    return jsonify(new_state.to_dict()), "201"


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_update(state_id):
    """Updates state object."""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "created_at", "update_at"]:
            setattr(state_obj, key, value)
    state_obj.save()
    return jsonify(state_obj.to_dict())
