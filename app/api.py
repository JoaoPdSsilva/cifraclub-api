from flask import Flask, json
from flask_cors import CORS
from cifraclub import CifraClub
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return app.response_class(
        response=json.dumps({'api': 'Cifra Club API'}),
        status=200,
        mimetype='application/json'
    )

@app.route('/song/<artist>/<song>')
def get_cifra(artist, song):
    cifraclub = CifraClub()
    return app.response_class(
        response=json.dumps(
            cifraclub.cifra(artist, song),
            ensure_ascii=False
        ),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT', 3000))
