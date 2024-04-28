#!/usr/bin/python3
'''a new view for State objects that handles all default RESTFul API actions'''
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """Retrieves the list of all State objects"""
    amenity = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenity)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a State object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a State object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Creates a State"""
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if 'name' not in request_data:
        abort(400, "Missing name")
    new_amenity = Amenity(**request_data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,  methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a State object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    for k, v in request_data.items():
        if k not in ('id', 'created_at', 'updated_at'):
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 200
