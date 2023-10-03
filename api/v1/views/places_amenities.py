#!/usr/bin/python3
"""Module for views API places amenities endpoints."""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False)
def place_amenities(place_id):
    """Retrieve all places amenities."""
    place_id = "{}.{}".format(Place.__name__, place_id)
    place_obj = storage.all(Place).get(place_id)
    if place_obj is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = [
            amenity.to_dict() for amenity in place_obj.amenities
        ]
    else:
        amenities = [
            storage.all().get()[amenity_id].to_dict() for amenity_id in place_obj.amenity_ids
        ]

    return jsonify(amenities)

@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def place_amenity_del(place_id, amenity_id):
    """Delete place amenity."""
    place_id = "{}.{}".format(Place.__name__, place_id)
    place_obj = storage.all(Place).get(place_id)
    if place_obj is None:
        abort(404)

    amenity_id = "{}.{}".format(Amenity.__name__, place_id)
    amenity_obj = storage.all(Amenity).get(amenity_id)
    if amenity_obj is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity_obj not in place_obj.amenities:
            abort(404)
        place_obj.amenities.remove(amenity_obj)
    else:
        if amenity_id not in place_obj.amenity_ids:
            abort(404)
        place_obj.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({})

@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def place_amenity_add(place_id, amenity_id):
    """Add place amenity object."""
    place_id = "{}.{}".format(Place.__name__, place_id)
    place_obj = storage.all(Place).get(place_id)
    if place_obj is None:
        abort(404)

    amenity_id = "{}.{}".format(Amenity.__name__, place_id)
    amenity_obj = storage.all(Amenity).get(amenity_id)
    if amenity_obj is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_dict())
        else:
            place_obj.amenities.append(amenity_obj)
    else:
        if amenity_id in place_obj.amenity_ids:
            return jsonify(amenity_obj.to_dict())
        else:
            place_obj.amenity_ids.append(amenity_id)
    place_obj.save()
    return jsonify(amenity_obj.to_dict()), "201"