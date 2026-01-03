"""API Module"""

import os
from flask import Flask, jsonify
from cifraclub import CifraClub

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    """Home route"""
    return jsonify({
        "api": "Cifra Club API",
        "status": "online"
    })

@app.route("/song/<artist>/<song>")
def get_cifra(artist, song):
    """Get cifra by artist and song"""

    cifra_client = CifraClub()
    result = cifra_client.cifra(artist, song)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
