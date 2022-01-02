from flask import Blueprint, jsonify, Response, request
import pymongo
import json
from bson import json_util
from pymongo import MongoClient

countries_api = Blueprint('countries_api', __name__)

def _get_db_client():
    mongo = pymongo.MongoClient(
        host = "sprc_mongodb",
        port = 27017
    )
    db = mongo.sprc
    return db['countries']

@countries_api.route("/api/countries", methods=['POST'])
def add_country():
    mongo = _get_db_client()

    counts = mongo.estimated_document_count()

    object_to_add = request.json

    country_name = object_to_add.get("nume", None)

    if country_name:
        check_if_exists = mongo.find_one({"nume": country_name})
        if check_if_exists:
            return Response(status=409)
        else:
            if object_to_add.get("lat") and object_to_add.get("lon"):
                object_to_add["id"] = counts
                mongo.insert_one(object_to_add)
                return json_util.dumps({"id": counts}), 201

    return Response(status=400)

@countries_api.route('/api/countries', methods=["GET"])
def get_countries():
    mongo = _get_db_client()
    countries = []
    projection = {
        "_id": 0
    }
    response = mongo.find({}, projection = projection)

    for it in response:
        countries.append(it)

    return Response(json.dumps(countries), status=200)

@countries_api.route("/api/countries/<id>", methods=["PUT"])
def edit_country(id):
    mongo = _get_db_client()
    mongo_result = mongo.find_one({"id": int(id)})
    if mongo_result:
        req_data = request.json
        req_id = req_data.get("id", None)

        if req_id:
            if int(req_id) != int(id):
                return Response(status=400)
        else:
            return Response(status=400)

        country_name = req_data.get("nume", None)
        lat = req_data.get("lat", None)
        lon = req_data.get("lon", None)

        if req_id and country_name and lat and lon:
            new_values = {
                "$set": {
                    "nume": country_name,
                    "lat": lat,
                    "lon": lon
                }
            }
            mongo.update_one(mongo_result, new_values)
            return Response(status=200)
        else:
            return Response(status = 400)

    return Response(status=404)

@countries_api.route("/api/countries/<id>", methods=["DELETE"])
def delete_country(id):
    mongo = _get_db_client()
    mongo_result = mongo.find_one({"id": int(id)})
    if mongo_result:
        mongo.delete_one(mongo_result)
        return Response(status=200)

    return Response(status=404)