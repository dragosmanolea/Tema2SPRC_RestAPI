from flask import Flask
import pymongo

def _get_db_client():
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.sprc
    return db


app = Flask(__name__)

@app.route("/", methods=['GET'])
def hehe():
    db_client = _get_db_client()
    user = {
        "name": "Dragos bossu",
        "functie": "sofer de bmw"
    }
    try:
        db_client.users.insert_one(user)
    except Exception as e:
        print(e)

    return "boss"


if __name__ == "__main__":
    app.run(port=8080, debug=True)