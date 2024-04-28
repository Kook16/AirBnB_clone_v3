#!/usr/bin/python3
'''a new view for State objects that handles all default RESTFul API actions'''
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """Creates a Place"""
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if storage.get(City, city_id) is None:
        abort(404)
    if 'user_id' not in request_data:
        abort(400, "Missing user_id")
    if storage.get(User, request_data['user_id']) is None:
        abort(404)
    if 'name' not in request_data:
        abort(400, "Missing name")
    new_place = Place(**request_data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 strict_slashes=False,  methods=['PUT'])
def update_place(place_id):
    """Updates a City object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    for k, v in request_data.items():
        if k not in ('id', 'created_at', 'updated_at', 'user_id', 'city_id'):
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
