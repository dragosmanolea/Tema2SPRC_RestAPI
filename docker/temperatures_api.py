from flask import Blueprint, jsonify, Response, request
import pymongo
import json
from pymongo import MongoClient
from datetime import datetime

temperatures_api = Blueprint('temperatures_api', __name__)

def _get_db_client():
    mongo = pymongo.MongoClient(
        host = "sprc_mongodb",
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

    check_if_idOras_exists = mongo['cities'].find_one({"id": int(idOras)})
    
    if not check_if_idOras_exists:
        return Response(status=404)

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
        host = "sprc_mongodb",
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
    args = request.args
    _from = args.get('from', None)
    until = args.get('until', None)
    temps = []
    id = int(idOras)

    mongo = pymongo.MongoClient(
        host = "sprc_mongodb",
        port = 27017
    )

    db = mongo.sprc

    aux_temps = db['temperatures'].find({"idOras": id}, {"_id": 0})
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

@temperatures_api.route("/api/temperatures/countries/<id_tara>", methods=["GET"])
def getTemperaturesByCountry(id_tara):
    temps = []
    args = request.args
    _from = args.get('from', None)
    until = args.get('until', None)
    temps = []
    idTara = int(id_tara)
    
    mongo = pymongo.MongoClient(
        host = "sprc_mongodb",
        port = 27017
    )

    db = mongo.sprc

    res = db['temperatures'].find({}, {"_id": 0})

    for it in res:
        idOras = int(it.get("idOras"))
        idOras += 1
        cities = db['cities'].find({"id": idOras, "idTara": idTara}, {"_id": 0})
        for jt in cities:
            if _from and until:
                currentTime = it.get("time", None)
                if _from <= currentTime and until >= currentTime:
                    temps.append(it)
            elif _from:
                currentTime = it.get("time", None)
                if _from <= currentTime:
                    temps.append(it)
            elif until:
                currentTime = it.get("time", None)
                if until >= currentTime:
                    temps.append(it)
            else:
                temps.append(it)

    return Response(json.dumps(temps), status=200)

@temperatures_api.route("/api/temperatures/<id>", methods=["PUT"])
def changeTemperature(id):
    mongo = pymongo.MongoClient(
        host = "sprc_mongodb",
        port = 27017
    )

    db = mongo.sprc
    id = int(id)
    res = db['temperatures'].find_one({"id": id}, {"_id": 0})
    
    if res:
        req = request.json
        idOras = req.get("idOras", None)
        new_val = req.get("valoare", None)

        if idOras is None or new_val is None:
            return Response(status=400)
        else:
            new_values = {
                "$set": {
                    "valoare": int(new_val),
                    "idOras": int(idOras)
                }
            }
            db['temperatures'].update_one(res, new_values)
    else:
        return Response(status=404)

    return Response(status=200)

@temperatures_api.route('/api/temperatures/<id>', methods=['DELETE'])
def deleteTemp(id):
    mongo = pymongo.MongoClient(
        host = "sprc_mongodb",
        port = 27017
    )

    db = mongo.sprc
    id = int(id)
    if id != id:
        return Response(status=400)
    
    res = db['temperatures'].find_one({"id": id}, {"_id": 0})
    if res:
        db.delete_one(res)
        return Response(status=200)
    
    return Response(status=404)