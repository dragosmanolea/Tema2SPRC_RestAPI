from flask import Blueprint, jsonify, Response, request
import pymongo
import json
from pymongo import MongoClient

temperatures_api = Blueprint('temperatures_api', __name__)

def _get_db_client():
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017
    )
    db = mongo.sprc
    return db['temperatures']