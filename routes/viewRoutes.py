from flask import make_response, jsonify, request, render_template, session, redirect, url_for
from app import app, jwt
import json, requests
from flask_jwt_extended import jwt_required



@app.route('/', methods=['GET'])
def index():
    return render_template('pre.html')


# @app.route('/', methods=['GET'])
# def index():
#     req = requests.get('http://localhost:5000/api/rooms')
#     data = req.content;
#     json_data = json.loads(data)
#     return render_template('test.html', rooms=json_data['rooms'])



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


# Front end /login route handler. Send request to /api/login with json data
@app.route('/login', methods=['GET', 'POST'])
def login(msg=''):

    # If post request is made
    if request.method == 'POST':

        # Get form data. Convert to dictionary
        data = request.form.to_dict()

        # Send acutal request to /api/login with dictionary data. Get response
        req = requests.post(url = 'http://localhost:5000/api/login', json=data)

        # Convert the content which contains token of the response to json. Save to data
        data = req.content
        json_data = json.loads(data)
        

        # check for token in response
        if 'token' in json_data:
        
            # add token to session
            session['token'] = json_data['token']

            # redirect to /profile
            return redirect('/profile')

        return render_template('test_login.html', msg=json_data['message'])

    return render_template('login.html', msg='')

@jwt_required
@app.route('/profile', methods=['GET'])
def profile():

    # if not 'token' in session:
    #     # Not logged in
    #     return redirect(url_for('login', msg='Please Log in'))
    
    # access_token = session['token']


    data = req.content
    print(data)
    json_data = json.loads(data)
    return render_template('test_profile.html', data=json_data['sub'])

@app.route('/logout', methods=['GET'])
def logout():
    del session['token']

    return redirect('/')