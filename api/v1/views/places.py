from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.user import User
from models.place import Place


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def places(city_id):
    """Retrieve all places objects."""
    if city_id == None:
        abort(404)

    place_objs = storage.all(Place)
    output = []
    for place in place_objs.values():
        if city_id == place.city_id:
            output.append(place.to_dict())
    return jsonify(output)

@app_views.route("/places/<place_id>", strict_slashes=False)
def place_id(place_id):
    """Retrieve place object."""
    if place_id == None:
        abort(404)
    place_id = "{}.{}".format(Place.__name__, place_id)
    try:
        place_obj = storage.all(Place)[place_id]
    except KeyError:
        abort(404)

    return jsonify(place_obj.to_dict()), "OK"

@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def place_id_del(place_id):
    """Deletes place object."""
    if place_id == None:
        abort(404)
    place_id = "{}.{}".format(Place.__name__, place_id)
    try:
        place_obj = storage.all(Place)[place_id]
    except KeyError:
        abort(404)

    storage.delete(place_obj)
    return jsonify({}), "200"

@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def place_add(city_id):
    """Add city."""
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    if "name" not in body.keys():
        abort(400, "Missing name")
    if "user_id" not in body.keys():
        abort(400, "Missing user_id")
    user_id =body["user_id"]
    name = body["name"]
    try:
        user =  storage.all(User)[user_id]
    except KeyError:
        abort(404)
    try:
        city =  storage.all(User)[city_id]
    except KeyError:
        abort(404)
    new_place = Place(name=name, user_id=user.id, city_id=city.id)

    storage.new(new_place).save()
    return jsonify(new_place.to_dict()), "201"

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def place_update(place_id):
    """Updates place object."""
    if place_id is None:
        abort(404)
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    place_id = "{}.{}".format(Place.__name__, place_id)
    try:
        place_obj = storage.all(Place)[place_id]
    except KeyError:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "user_id", "city_id", "created_at", "update_at"]:
            setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_dict()), "200"
