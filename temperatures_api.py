from flask import Blueprint, jsonify, Response, request
import pymongo
import json
from pymongo import MongoClient
from datetime import datetime

temperatures_api = Blueprint('temperatures_api', __name__)

def _get_db_client():
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017
    )
    db = mongo.sprc
    return db['temperatures']

@temperatures_api.route('/api/temperatures', methods=['POST'])
def add_temperature():
    mongo = _get_db_client()
    counts = mongo.estimated_document_count()

    req_data = request.get_json()
    idOras = req_data.get("idOras", None)
    valoare = req_data.get("valoare", None)
    date = datetime.now().strftime("%Y-%m-%d")

    if idOras is not None and valoare:
        if type(valoare) == str:
            valoare = float(valoare)
        
        # check if valoare != nan
        # valoare can be nan if valoare is not a number above
        if valoare != valoare:
            return Response(status=409)

        mongo.insert_one({
            "id": counts,
            "idOras": idOras,
            "valoare": valoare,
            "time": date
        })
        return Response({"id": counts}, status=201)

    return Response(status=400)

@temperatures_api.route("/api/temperatures", methods=["GET"])
def get_temperatures():
    args = request.args

    lat = args.get('lat', {"$exists": True})
    lon = args.get('lon', {"$exists": True})
    _from = args.get('from', None)
    until = args.get('until', None)

    if type(lat) == str:
        lat = float(lat)

    if type(lon) == str:
        lon = float(lon)

    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017
    )

    db = mongo.sprc
    
    res = db['countries'].find(
        {
            "lat": lat,
            "lon": lon,
        },
        {"_id":0}
    )

    temps = []

    for it in res:
        id = it.get("id", None)
        id -= 1
        aux_temps = db['temperatures'].find({"idOras": int(id)}, {"_id": 0})
        for jt in aux_temps:
            if _from and until:
                currentTime = jt.get("time", None)
                if _from <= currentTime and until >= currentTime:
                    temps.append(jt)
            elif _from:
                currentTime = jt.get("time", None)
                if _from <= currentTime:
                    temps.append(jt)
            elif until:
                currentTime = jt.get("time", None)
                if until >= currentTime:
                    temps.append(jt)
            else:
                temps.append(jt)

    return Response(json.dumps(temps), status=200)

@temperatures_api.route("/api/temperatures/cities/<idOras>", methods=["GET"])
def getTemperaturesByCity(idOras):
    pass