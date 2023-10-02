from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def amenities():
    """Retrieve all amenity objects."""
    amenity_objs = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenity_objs.values()])

@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def amenities_id(amenity_id):
    """Retrieve amenity object."""
    if amenity_id == None:
        abort(404)
    amenity_id = "{}.{}".format(Amenity.__name__, amenity_id)
    try:
        amenity_obj = storage.all(Amenity)[amenity_id]
    except KeyError:
        abort(404)

    return jsonify(amenity_obj.to_dict()), "OK"

@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def amenity_id_del(amenity_id):
    """Deletes amenity object."""
    if amenity_id == None:
        abort(404)
    amenity_id = "{}.{}".format(Amenity.__name__, amenity_id)
    try:
        amenity_obj = storage.all(Amenity)[amenity_id]
    except KeyError:
        abort(404)

    storage.delete(amenity_obj).save()
    return jsonify({}), "200"

@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_add():
    """Add amenity."""
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    if "name" not in body.keys():
        abort(400, "Missing name")
    name = body["name"]
    new_amenity = Amenity(name=name)
    storage.new(new_amenity).save()
    return jsonify(new_amenity.to_dict()), "201"

@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def amenity_update(amenity_id):
    """Updates amenity object."""
    if amenity_id is None:
        abort(404)
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    amenity_id = "{}.{}".format(Amenity.__name__, amenity_id)
    try:
        amenity_obj = storage.all(Amenity)[amenity_id]
    except KeyError:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "created_at", "update_at"]:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), "200"
