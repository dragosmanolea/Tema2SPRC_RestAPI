from flask import Flask
from cities_api import cities_api
from countries_api import countries_api
from temperatures_api import temperatures_api

app = Flask(__name__)

app.register_blueprint(cities_api)
app.register_blueprint(countries_api)
app.register_blueprint(temperatures_api)

if __name__ == "__main__":
    app.run(port=8081, debug=True)