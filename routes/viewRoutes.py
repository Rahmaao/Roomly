from flask import make_response, jsonify, request, render_template, redirect, url_for
from app import app, session
import json, requests
from routes.authRoutes import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, set_access_cookies
from database import User



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
        json_data = json.loads(req.content)

        # Since we are setting it in tokens, we need a differnt way to check.


        # check for token in response
        if 'token' in json_data:
            # add token to session
            session['token'] = json_data['token']

            response = redirect('/profile')

            # Set this always
            set_access_cookies(response, session['token'])

            return response
  
        return render_template('login.html', msg=json_data['message'])

    return render_template('login.html', msg='')


@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():

    # if not 'token' in session:
    #     # Not logged in
    #     return redirect(url_for('login', msg='Please Log in'))
    
    # # access_token = session['token']
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user.username =='admin':
        session['user'] = 'admin'
        return redirect('/admin')

    # data = req.content
    # print(data)
    # json_data = json.loads(data)
    return render_template('test_profile.html', data=user.username)
@app.route('/logout', methods=['GET'])
def logout():
    req = requests.get('http://localhost:5000/api/logout')
    return redirect('/')