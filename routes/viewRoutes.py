from flask import make_response, jsonify, request, render_template
from app import app
import json, requests


@app.route('/', methods=['GET'])
def index():
    req = requests.get('http://localhost:5000/api/rooms')
    data = req.content;
    json_data = json.loads(data)
    print(json_data)
    return render_template('test.html', data=json_data['rooms'])