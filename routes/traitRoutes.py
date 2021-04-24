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

api = Api(app)


class TraitList(Resource):
    """
    Resource for /api/hostels endpoint
    """
    def get(self):
        traits = Trait.query.all()
        traits = TraitSchema(many=True).dump(traits)

        return jsonify({
            "traits" : traits,
            "results": len(traits)
        })

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
    def get(self, id):
        trait = Trait.query.get_or_404(id)
        trait = TraitSchema().dump(trait)

        return jsonify({
            'trait' : trait
        })
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
