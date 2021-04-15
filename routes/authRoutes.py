from models.User import User, UserSchema
from controllers import auth
from flask import make_response, jsonify, request, session
from marshmallow.exceptions import *
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


from app import app


jwt = JWTManager(app)

@app.route('/api/login', methods=['POST'])
def authenticate_user():
    # Get json data from request
    data = request.json


    # query the User model for the username sent. Store the result in
    # current_user
    current_user = User.find_by_username(data['username'])

    # We'll now write a bunch of tests for current. If it fails anyone,
    # We'll return an error.

    # Test if user not on DB
    if not current_user:
        return {
            'message': 'No user with that name'
        }, HTTPStatus.FORBIDDEN

    # Test if password is not correct
    if not User.check_password(data['password'], current_user.password):
        return {
            'message': 'Check username or password'
        }, HTTPStatus.FORBIDDEN


    # All tests were passed. Yay! User identity confirmed 

    access_token =  create_access_token(identity=data['username'])

    # session['access_token'] = access_token

    return {
        "message": 'Logged in',
        "token": access_token
    }, HTTPStatus.ACCEPTED
    # All tests were passed. Yay! User identity confirmed 
    # return {
    # #     'message': 'User exists. Yay'
    # # }, HTTPStatus.ACCEPTED

@app.route('/api/register', methods=['POST'])
def register_user():

    data = request.json
    user_schema = UserSchema() # This is the only line that changes
    try:
        user = user_schema.load(data)
        result = user_schema.dump(user.create())

    except Exception as exec:
        # print(exec)
        return {
            'message' : exec.__str__(),
        }, HTTPStatus.BAD_REQUEST


    return make_response(jsonify({"user": result }))
