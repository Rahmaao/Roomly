'''This handles all request to /users route.
Imports  User, UserSchema
'''

from database import User, UserSchema, db, Trait
from flask import make_response, jsonify, request
from marshmallow.exceptions import *
from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager, current_user
from controllers.factoryController import get_all, create_one, get_one, delete_one
from routes.authRoutes import jwt, admin_required


api = Api(app)


class UsersList(Resource):

    @jwt_required()
    def get(self):
        data = get_all('user')
        return jsonify({
           'users' : data,
           'results' : len(data) 
        })

    
    #locked ot admin
    @admin_required()
    def post(self):

        # Parse necessary arguments
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('password')

        # Hash password

        data = parser.parse_args()

        user = create_one('user', data)

        return jsonify({
            'user': user
        })
class SingleUser(Resource):

    @jwt_required()
    def get(self, id):
        user = get_one('user', id)
        return {
            'user' : user
        }
    def patch(self, id):
        pass

    @admin_required()
    def delete(self, id):
        return delete_one('user', id)

class ChangeUserPassword(Resource):
    def patch(self, id):
        data = request.json
        user = get_one('user', id)
        if data['password'] != data['confirm_password']:
            return jsonify({
                'message' : 'Passwords are not the same'
            })
        try:
            hashed_password = generate_password_hash(data['password'])
            # Set user to hashed
            user.password = hashed_password
            db.session.commit()
        except Exception as e:
            responseObject = {
                'status' : 'fail',
                'message': 'Some error occured/ Please try again'
            }
            return jsonify(responseObject),202
        return jsonify({
            'message': 'Some error occured',
        }), 202


class TraitOnUser(Resource):
    def patch(self, id):

        data = request.json
        # Call factory methods to return model objects
        user = get_one('user', id, 'obj')
        trait = get_one('trait', data['trait'], 'obj')
        # Most likely, we'll get a list of traits.
        # We'll have to iterate through the list-- for validation?
        # OR join lists.

        user.traits.append(trait)
        db.session.commit()

        user = get_one('user', id)

        return jsonify({
            'user' : user
        })




api.add_resource(UsersList, '/api/users')
api.add_resource(SingleUser, '/api/users/<id>')
api.add_resource(TraitOnUser, '/api/users/<id>/traits')
