#!/usr/bin/python3
"""This module created API of the amenities"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import request, make_response, jsonify

met = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('amenities', methods=met, strict_slashes=True)
@app_views.route('amenities/<amenity_id>', methods=met, strict_slashes=True)
def amenities(amenity_id=None):
    """This method check the type request method"""
    if request.method == 'GET':
        if amenity_id:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                return jsonify(amenity.to_dict())
            return make_response(jsonify({"error": "Not found"}), 404)
        objs = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
        return jsonify(objs)

    if request.method == 'DELETE':
        if amenity_id:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                storage.delete(amenity)
                storage.save()
                return make_response(jsonify({}), 200)
            return make_response(jsonify({"error": "Not found"}), 404)

    if request.method == 'POST':
        content = request.get_json()
        if content:
            if "name" not in content:
                return make_response(jsonify({"error": "Missing name"}), 400)
            new = Amenity(**content)
            new.save()
            return make_response(jsonify(new.to_dict()), 200)
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if request.method == 'PUT':
        if amenity_id:
            content = request.get_json()
        if not content:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            for key, value in content.items():
                if key != "id" and key != "created_at" and key != "update_at":
                    setattr(amenity, k, value)
                    storage.save()
                    return make_response(jsonify(amenity.to_dict()), 200)
        return make_response(jsonify({"error": "Not found"}), 404)
        return make_response(jsonify({"error": "Not found"}), 404)