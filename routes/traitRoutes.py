''''This handles all requests to /rooms route.
imports Rooms, RoomSchema model
'''

from database import Trait, TraitSchema, db
from flask import make_response, jsonify, request
from flask_restful import reqparse, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import *
from http import HTTPStatus
from app import app
from flask_jwt_extended import jwt_required
from routes.authRoutes import jwt

api = Api(app)


class TraitList(Resource):
    """
    Resource for /api/hostels endpoint
    """

    @jwt_required()
    def get(self):
        traits = Trait.query.all()
        traits = TraitSchema(many=True).dump(traits)

        return jsonify({
            "traits" : traits,
            "results": len(traits)
        })

    #Admin only
    @admin_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('trait')

        data = parser.parse_args()

        trait = TraitSchema().load(data)
        trait = TraitSchema().dump(trait.create())

        return jsonify({
            'trait' : trait
        })

class SingleTrait(Resource):
    """ 
    Resource for getting a single Trait
    """

    @jwt_required()
    def get(self, id):
        trait = Trait.query.get_or_404(id)
        trait = TraitSchema().dump(trait)

        return jsonify({
            'trait' : trait
        })

     #Admin   
    @admin_required()
    def patch(self, id):
        trait = Trait.query.get_or_404(id)

        parser = reqparse.RequestParser()
        parser.add_argument('trait')
        data = parser.parse_args()

        if data['trait'] != None:
            trait.trait = data['trait']

        db.session.commit()

        trait = TraitSchema().dump(trait)
        return ({
            'trait' : trait
        })



    def delete(self, id):
        trait = Trait.query.get_or_404(id)

        db.session.delete(trait)
        db.session.commit()

        return '', 204

    
api.add_resource(TraitList, '/api/traits')
api.add_resource(SingleTrait, '/api/traits/<id>')
