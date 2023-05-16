from flask import Flask, jsonify, request
from flask_cors import CORS
from main import calculate

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['POST'])
def get_params():
    request_data = request.get_json()
    routes = calculate(request_data)
    return jsonify(routes)

app.run(port=7001)