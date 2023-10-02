from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def cities(state_id):
    """Retrieve all state objects."""
    if state_id == None:
        abort(404)

    city_objs = storage.all(City)
    output = []
    for city in city_objs.values():
        if state_id == city.state_id:
            output.append(city.to_dict())
    return jsonify(output)

@app_views.route("/cities/<city_id>", strict_slashes=False)
def cities_id(city_id):
    """Retrieve city object."""
    if city_id == None:
        abort(404)
    city_id = "{}.{}".format(City.__name__, city_id)
    try:
        city_obj = storage.all(City)[city_id]
    except KeyError:
        abort(404)

    return jsonify(city_obj.to_dict()), "OK"

@app_views.route("/cities/<city_id>",
                 methods=["DELETE"], strict_slashes=False)
def city_id_del(city_id):
    """Deletes city object."""
    if city_id == None:
        abort(404)
    city_id = "{}.{}".format(City.__name__, city_id)
    try:
        city_obj = storage.all(City)[city_id]
    except KeyError:
        abort(404)

    storage.delete(city_obj).save()
    return jsonify({}), "200"

@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def city_add(state_id):
    """Add state."""
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    if "name" not in body.keys():
        abort(400, "Missing name")
    name = body["name"]
    new_city = City(name=name, state_id=state_id)

    storage.new(new_city).save()
    return jsonify(new_city.to_dict()), "201"

@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_update(city_id):
    """Updates city object."""
    if city_id is None:
        abort(404)
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    city_id = "{}.{}".format(City.__name__, city_id)
    try:
        city_obj = storage.all(City)[city_id]
    except KeyError:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "created_at", "update_at"]:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict()), "200"
