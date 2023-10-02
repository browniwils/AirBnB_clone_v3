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
    if state_id == None:
        abort(404)
    state_id = "{}.{}".format(State.__name__, state_id)
    try:
        state_obj = storage.all(State)[state_id]
    except KeyError:
        abort(404)

    return jsonify(state_obj.to_dict()), "OK"

@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def state_id_del(state_id):
    """Deletes state object."""
    if state_id == None:
        abort(404)
    state_id = "{}.{}".format(State.__name__, state_id)
    try:
        state_obj = storage.all(State)[state_id]
    except KeyError:
        abort(404)

    storage.delete(state_obj).save()
    return jsonify({}), "200"

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_add():
    """Add a state."""
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    if "name" not in body.keys():
        abort(400, "Missing name")
    name = body["name"]
    new_state = State(name=name)
    storage.new(new_state).save()
    return jsonify(new_state.to_dict()), "201"

@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_update(state_id):
    """Updates state object."""
    if state_id is None:
        abort(404)
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    state_id = "{}.{}".format(State.__name__, state_id)
    try:
        state_obj = storage.all(State)[state_id]
    except KeyError:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "created_at", "update_at"]:
            setattr(state_obj, key, value)
    state_obj.save()
    return jsonify(state_obj.to_dict()), "200"
