#!/usr/bin/python3
'''a new view for User objects that handles all default RESTFul API actions'''
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    user = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Creates a User"""
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if 'email' not in request_data:
        abort(400, "Missing email")
    if 'password' not in request_data:
        abort(400, "Missing password")
    new_user = User(**request_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,  methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    for k, v in request_data.items():
        if k not in ('id', 'created_at', 'updated_at', 'email'):
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
