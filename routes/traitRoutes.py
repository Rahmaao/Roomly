''''This handles all requests to /rooms route.
imports Rooms, RoomSchema model
'''

from models.Trait import Traits, TraitsSchema, db
from flask import make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import *
from http import HTTPStatus
from app import app

# db = SQLAlchemy(app)


trait_schema = TraitsSchema()

# Use the route for  GET request on /traits
@app.route('/api/traits', methods=['GET'])
def get_traits():

    get_traits = Traits.query.all()
    trait_schema = TraitsSchema(many=True)
    try:
        traits = trait_schema.dump(get_traits)
    except ValidationError as exec:
        return {
            'message' : "Validation errors", 'errors': exec.messages
        }, HTTPStatus.BAD_REQUEST
    
    return make_response(jsonify({"traits": traits, "results": len(traits)}))

# Use this route for POST request on /rooms
@app.route('/api/traits', methods=['POST'])
def add_traits():
    #To be refactored

    # get json data from request
    data = request.json

    try: 
        trait = trait_schema.load(data)
    except ValidationError as exec:
        return {
            'message' : "Validation errors", 'errors': exec.messages
        }, HTTPStatus.BAD_REQUEST
    result = trait_schema.dump(trait.create())

    return make_response(jsonify({"trait": result}))


@app.route('/api/traits/<id>', methods=['GET'])
def get_trait_by_id(id):

    # Query a trait
    get_trait = Traits.query.get(id)
    result = trait_schema.dump(get_trait)

    # Test for result
    if not result:
        return make_response(jsonify({
            "message": "No trait with that id."
        }))

    # Return trait
    return trait_schema.dump(get_trait)

@app.route('/api/traits/<id>', methods=['DELETE'])
def delete_trait_by_id(id):

    # Query trait data
    get_trait = Traits.query.get(id)
    trait = trait_schema.dump(get_trait)

    # If empty result, trait with ID doesn't exist
    if not trait:
        return make_response(jsonify({ 'message' : 
        'Trait with this ID does not exist'}))
        
    db.session.delete(get_trait)
    db.session.commit()

    # Send response
    return '', 204




@app.route('/api/traits/<id>', methods=['PATCH'])
def update_trait_by_id(id):

    # The difference between a PATCH and PUT
    # request is that PATCH modifies entry. Meanwhile
    # PUT actualaly clears the old entry and reenters the values

    # Get json data from response

    data = request.json
    get_trait = Traits.query.get(id)

    # Test for result
    if not get_trait:
        return make_response(jsonify({
            "message": "No trait with that id."
        }))


    if 'traits' in data:
        get_room.name = data['traits']

    db.session.commit()

    return trait_schema.dump(get_trait)
    

