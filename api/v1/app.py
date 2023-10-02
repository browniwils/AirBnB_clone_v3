#!/usr/bin/python3

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv



app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

@app.teardown_appcontext
def teardown(self):
    """Close storage session."""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handles not found resources."""
    return jsonify(error="Not found"), 404

if __name__ == "__main__":

    HOST = getenv("HBNB_API_HOST")
    PORT = getenv("HBNB_API_PORT")

    if HOST == None:
        HOST = "0.0.0.0"
    if PORT == None:
        PORT = "5000"

    app.run(host=HOST, port=PORT, debug=True, threaded=True)