#!/usr/bin/python3
"""Module for views API place reviews endpoints."""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def reviews(place_id):
    """Retrieve all reviews objects."""
    place_obj = storage.get(Place, place_id)
    if place_obj == None:
        abort(404)

    return jsonify({[review.to_dict() for review in place_obj.reviews]})


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def review_id(review_id):
    """Retrieve review object."""
    review_obj = storage.get(Review, review_id)
    if review_obj == None:
        abort(404)

    return jsonify(review_obj.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def review_id_del(review_id):
    """Deletes review object."""
    review_obj = storage.get(Review, review_id)
    if review_obj == None:
        abort(404)

    review_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def review_add(place_id):
    """Add review."""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if "user_id" not in body.keys():
        abort(400, "Missing user_id")
    if "text" not in body.keys():
        abort(400, "Missing text")
    user_id = body["user_id"]
    user_obj =  storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    new_review = Review(**body)
    new_review.place_id = place_obj.id
    new_review.save()
    return jsonify(new_review.to_dict()), "201"


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def review_update(review_id):
    """Updates review object."""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")

    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "user_id", "place_id", "created_at", "update_at"]:
            setattr(review_obj, key, value)
    review_obj.save()
    return jsonify(review_obj.to_dict())
