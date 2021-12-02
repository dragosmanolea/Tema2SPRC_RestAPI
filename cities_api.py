from flask import Blueprint, jsonify, Response
import pymongo
import json
from bson import json_util

def _get_db_client():
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.sprc
    return db

cities_api = Blueprint('cities_api', __name__)

@cities_api.route("/v1/api/cities", methods=['GET'])
def get_cities():
    mongo = _get_db_client()
    result = mongo.users.find_one({"name": "Dragos bossu 2"})

    return json_util.dumps(result), 200


