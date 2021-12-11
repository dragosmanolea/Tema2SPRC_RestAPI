from flask import Blueprint, jsonify, Response, request
import pymongo
import json

def _get_db_client():
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017
    )
    db = mongo.sprc
    return db

cities_api = Blueprint('cities_api', __name__)

@cities_api.route("/api/cities", methods=['POST'])
def add_city():
    mongo = _get_db_client()
    col = mongo['cities']
    counts = col.estimated_document_count()
    req_data = request.json
    
    nume = req_data.get("nume", None)
    req_data["id"] = counts + 1

    if nume:
        check_if_exists = col.find_one({"nume": nume})

        if check_if_exists:
            return Response(status=409)
        else:
            # add city
            if req_data.get("lat", None) and req_data.get("lon", None):
                col.insert_one(req_data)
                return json_util.dumps({"id": counts}), 201
 
    return Response(status=400)

@cities_api.route("/api/cities", methods=["GET"])
def get_cities():
    mongo = _get_db_client()
    col = mongo['cities']
    cities = []
    response = col.find({}, projection = {
        "_id":0
    })

    for it in response:
        cities.append(it)

    return Response(json.dumps(cities), status=200)

@cities_api.route("/api/cities/coutry/<idTara>", methods=["GET"])
def get_city_by_country(idTara):
    mongo = _get_db_client()
    col = mongo['cities']
    cities = []
    response = col.find({
        "idTara": int(idTara)
    }, projection = {
        "_id":0
    })

    for it in response:
        cities.append(it)

    return Response(json.dumps(cities), status=200)

@cities_api.route("/api/cities/<id>", methods=["PUT"])
def update_city(id):
    mongo = _get_db_client()
    col = mongo['cities']
    mongo_result = col.find_one({"id": int(id)})
    if mongo_result:
        req_data = request.json
        req_id = req_data.get("id", None)

        if req_id:
            if int(req_id) != int(id):
                return Response(status=400)
        else:
            return Response(status=400)

        city_name = req_data.get("nume", None)
        lat = req_data.get("lat", None)
        lon = req_data.get("lon", None)
        idTara = req_data.get("idTara", None)
        if req_id and city_name and lat and lon and idTara:
            new_values = {
                "$set": {
                    "nume": city_name,
                    "lat": lat,
                    "lon": lon,
                    "idTara": idTara
                }
            }
            col.update_one(mongo_result, new_values)
            return Response(status=200)
        else:
            return Response(status = 400)

    return Response(status=404)

@cities_api.route("/api/cities/<id>", methods=["DELETE"])
def delete_city(id):
    mongo = _get_db_client()
    col = mongo['cities']
    mongo_result = col.find_one({"id": int(id)})
    if mongo_result:
        mongo.delete_one(mongo_result)
        return Response(status=200)

    return Response(status=404)