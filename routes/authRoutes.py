from database import User, UserSchema
from controllers import auth
from flask import make_response, jsonify, request, session
from marshmallow.exceptions import *
from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies, get_jwt, current_user
from app import app

api = Api(app)
jwt = JWTManager(app)


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
            additional_claims = {"id": user.id}
            response = jsonify({
                'message': 'login successful'
            })

            # Import access cookies
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            set_access_cookies(response, access_token)

            return response
        return {
            'message' : 'Invalid username or password.'
        }

class LogoutUser(Resource):
    def get(self):
        response = jsonify({"msg": "Logout successful"})
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