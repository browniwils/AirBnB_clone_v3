from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def reviews(place_id):
    """Retrieve all reviews objects."""
    if place_id == None:
        abort(404)
    place_id = "{}.{}".format(Place.__name__, place_id)
    try:
        place = storage.all(Place)[place_id]
    except KeyError:
        abort(404)

    review_objs = storage.all(Review)
    output = []
    for review in review_objs.values():
        if place.id == review.place_id:
            output.append(review.to_dict())
    return jsonify(output)

@app_views.route("/reviews/<review_id>", strict_slashes=False)
def review_id(review_id):
    """Retrieve review object."""
    if review_id == None:
        abort(404)
    review_id = "{}.{}".format(Review.__name__, review_id)
    try:
        review_obj = storage.all(Review)[review_id]
    except KeyError:
        abort(404)

    return jsonify(review_obj.to_dict()), "OK"

@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def review_id_del(review_id):
    """Deletes review object."""
    if review_id == None:
        abort(404)
    review_id = "{}.{}".format(Review.__name__, review_id)
    try:
        review_obj = storage.all(Review)[review_id]
    except KeyError:
        abort(404)

    storage.delete(review_obj).save()
    return jsonify({}), "200"

@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def review_add(place_id):
    """Add review."""
    if place_id is None:
        abort(404)
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    if "user_id" not in body.keys():
        abort(400, "Missing user_id")
    if "text" not in body.keys():
        abort(400, "Missing text")
    user_id =body["user_id"]
    name = body["name"]
    try:
        user =  storage.all(User)[user_id]
    except KeyError:
        abort(404)
    try:
        place =  storage.all(Place)[place_id]
    except KeyError:
        abort(404)
    new_review = Review(name=name, user_id=user.id, place_id=place.id)

    storage.new(new_review).save()
    return jsonify(new_review.to_dict()), "201"

@app_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def review_update(review_id):
    """Updates review object."""
    if review_id is None:
        abort(404)
    body = request.get_json()
    if body is None or (isinstance(body, dict) == False):
        abort(400, "Not a JSON")
    review_id = "{}.{}".format(Review.__name__, review_id)
    try:
        review_obj = storage.all(Review)[review_id]
    except KeyError:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "user_id", "place_id", "created_at", "update_at"]:
            setattr(review_obj, key, value)
    review_obj.save()
    return jsonify(review_obj.to_dict()), "200"
