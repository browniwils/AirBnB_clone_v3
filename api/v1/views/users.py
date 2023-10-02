from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def users():
    """Retrieve all user objects."""
    user_objs = storage.all(User)
    return jsonify([user.to_dict() for user in user_objs.values()])

@app_views.route("/users/<user_id>", strict_slashes=False)
def users_id(user_id):
    """Retrieve user object."""
    if user_id == None:
        abort(404)
    user_id = "{}.{}".format(User.__name__, user_id)
    try:
        user_obj = storage.all(User)[user_id]
    except KeyError:
        abort(404)

    return jsonify(user_obj.to_dict()), "OK"

@app_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def user_id_del(user_id):
    """Deletes user object."""
    if user_id == None:
        abort(404)
    user_id = "{}.{}".format(User.__name__, user_id)
    try:
        user_obj = storage.all(User)[user_id]
    except KeyError:
        abort(404)

    storage.delete(user_obj).save()
    return jsonify({}), "200"

@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_add():
    """Adds a user."""
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    if "email" not in body.keys():
        abort(400, "Missing email")
    if "password" not in body.keys():
        abort(400, "Missing password")

    email = body["email"]
    password = body["password"]
    new_user = User(email=email, password=password)

    storage.new(new_user).save()
    return jsonify(new_user.to_dict()), "201"

@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def user_update(user_id):
    """Updates user object."""
    if user_id is None:
        abort(404)
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    user_id = "{}.{}".format(User.__name__, user_id)
    try:
        user_obj = storage.all(User)[user_id]
    except KeyError:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "email", "created_at", "update_at"]:
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), "200"
