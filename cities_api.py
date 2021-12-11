from flask import Blueprint, jsonify, Response, request
import pymongo
import json
from bson import json_util

def _get_db_client():
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017
    )
    db = mongo.sprc
    return db

cities_api = Blueprint('cities_api', __name__)

@cities_api.route("/api/cities", methods=['POST'])
def get_cities():
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

    