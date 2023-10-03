#!/usr/bin/python3
"""Module for views API places endpoints."""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def places(city_id):
    """Retrieve all places objects."""
    city_id = "{}.{}".format(City.__name__, city_id)
    city_obj = storage.all(City).get(city_id)
    if city_obj is None:
        abort(404)

    return jsonify( [place.to_dict() for place in city_obj.places])

@app_views.route("/places/<place_id>", strict_slashes=False)
def place_id(place_id):
    """Retrieve place object."""
    place_id = "{}.{}".format(Place.__name__, place_id)
    place_obj = storage.all(Place).get(place_id)
    if place_obj == None:
        abort(404)

    return jsonify(place_obj.to_dict())

@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def place_id_del(place_id):
    """Deletes place object."""
    place_id = "{}.{}".format(Place.__name__, place_id)
    place_obj = storage.all(Place)[place_id]
    if place_obj == None:
        abort(404)

    storage.delete(place_obj)
    storage.save()
    return jsonify({})

@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def place_add(city_id):
    """Add city."""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if "name" not in body.keys():
        abort(400, "Missing name")
    if "user_id" not in body.keys():
        abort(400, "Missing user_id")

    city_id = "{}.{}".format(City, city_id)
    city_obj = storage.all(City).get(city_id)
    if city_obj is None:
        abort(404)

    user_id = "{}.{}".format(User, body["user_id"])
    user_obj =  storage.all(User).get(user_id)
    if user_obj is None:
        abort(404)

    new_place = Place(**body)
    new_place.city_id = city_obj.id
    new_place.save()
    return jsonify(new_place.to_dict()), "201"

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def place_update(place_id):
    """Updates place object."""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    place_id = "{}.{}".format(Place.__name__, place_id)
    place_obj = storage.all(Place).get(place_id)
    if place_obj is None:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "user_id", "city_id", "created_at", "update_at"]:
            setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_dict())

@app_views.route("/place_search", methods=["POST"])
def place_search():
    """Retrieve all place object with search term."""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")

    if len(body):
        states = body.get("states", None)
        cities = body.get("cities", None)
        amenities = body.get("amenities", None)

        place_list = []
        if states is not None:
            states_obj = [
                storage.all(State).get(state_id) for state_id in states]
            for state in states_obj:
                if state is not None:
                    for city in state.cities:
                        if city is not None:
                            for place in city.places:
                                place_list.append(place)
        if cities is not None:
            cities_obj = [
                storage.all(City).get(city_id) for city_id in cities]
            for city in cities_obj:
                if city is not None:
                    for place in city.places:
                        if place not in place_list:
                            place_list.append(place)
        if amenities is not None:
            if place_list is None:
                place_list = storage.all(Place).values()
            amenities_obj = [
                storage.all(Amenity).get(amenity_id) for amenity_id in amenities]
            place_list = [
                place for place in place_list
                if all([amenity in place.amenities
                        for amenity in amenities_obj])]

        all_places = []
        for place in place_list:
            place.to_dict().pop("amenities", None)
            all_places.append(place)

        return jsonify(all_places)