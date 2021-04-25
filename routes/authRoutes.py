from database import User, UserSchema
from controllers import auth
from functools import wraps
from flask import make_response, jsonify, request
from marshmallow.exceptions import *
from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, jwt_required, JWTManager, set_access_cookies, 
unset_jwt_cookies, get_jwt, current_user, verify_jwt_in_request)
from app import app, session

api = Api(app)
jwt = JWTManager(app)


# Jwt custom decorator for admin access
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if 'isAdmin' in claims:
                return fn(*args, **kwargs)
            return {"msg":"Admins only!"}, 403
        return decorator
    return wrapper


class RegisterUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('password')
        parser.add_argument('confirm_password')
        data = parser.parse_args()

        if data['password'] != data['confirm_password']:
            return jsonify({
                'message' : 'Passwords are different'
            })


        user  = User.query.filter_by(username=data['username']).first()
        if not user:
            # new user
            # delete new password field
            del data['confirm_password']
            try:
                # hash password
                hashed_password = generate_password_hash(data['password'])
                # set password in data to hashed password
                data['password'] = hashed_password
                user = UserSchema().load(data)
                user.create()

                return jsonify({
                    'staus' : 'success',
                    'message' : 'Succesfully registered'
                })
            except Exception as e:
                responseObject = {
                    'status' : 'fail',
                    'message': 'Some error occured. Please try again'
                }
                return jsonify(responseObject), 202

        return jsonify({
            'message' : 'Error registering'
        }), 202


class LoginUser(Resource):
    def post(self):
        data = request.json
        # Check if user exists
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {
                'message' : 'Invalid username or password.'
            }

        # Check password
        if check_password_hash(user.password, data['password']):
            if user.username == 'admin':
                # session['user'] = 'admin'
                # session['admin'] = True
                additional_claims ={"isAdmin": True}
                access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            
            else:
                additional_claims = {"id": user.id}
                access_token = create_access_token(identity=user.id, additional_claims=additional_claims)


            # Import access cookies
            print(session)
            response = jsonify({
                'message': 'login successful',
                'token': access_token
            })

            set_access_cookies(response, access_token)

            return response
        return {
            'message' : 'Invalid username or password.'
        }

class LogoutUser(Resource):
    def get(self):
        response = jsonify({"msg": "Logout successful"})
        session.pop('user', None)
        session.pop('admin', None)
        unset_jwt_cookies(response)
        return response


@app.route('/api/myprofile', methods=['GET'])
@jwt_required()
def myprofile():
    return {'user': current_user.id}


api.add_resource(RegisterUser, '/api/register')
api.add_resource(LoginUser, '/api/login')
api.add_resource(LogoutUser, '/api/logout')
# api.add_resource(MYProfile, '/api/myprofile')