from flask import make_response, jsonify, request, render_template
from app import app
import json, requests


@app.route('/', methods=['GET'])
def index():
    req = requests.get('http://localhost:5000/api/rooms')
    data = req.content;
    json_data = json.loads(data)
    return render_template('test.html', rooms=json_data['rooms'])



# This is the route for /register
@app.route('/register', methods=['GET', 'POST'])
def register():
    # execute if there's a post request on route
    if request.method == 'POST':
        # Covert form data to a dictionary
        data = request.form.to_dict()
        # Send dictionary as json to api endpoint.
        result = requests.post(url = 'http://localhost:5000/api/users', json=data)

        # Check if code worked
        if(result.status_code == 200):
            # Ideally should log user in. TO be implemented
            return render_template('test_register.html', data='Registration successful')
        else:
            return render_template('test_register.html', data='There was an error somewhere')

        print(result.status_code);
    return render_template('test_register.html', data='')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()