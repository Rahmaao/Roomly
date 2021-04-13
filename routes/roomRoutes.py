''''This handles all requests to /rooms route.
imports Rooms, RoomSchmea model
'''

from models.Room import Room, RoomSchema
from flask import make_response, jsonify, request
from marshmallow.exceptions import *
from http import HTTPStatus
from app import app


# Use the route for  GET request on /rooms
@app.route('/api/rooms', methods=['GET'])
def get_rooms():

    get_rooms = Room.query.all()
    room_schema = RoomSchema(many=True)
    try:
        rooms = room_schema.dump(get_rooms)
    except ValidationError as exec:
        return {
            'message' : "Validation errors", 'errors': exec.messages
        }, HTTPStatus.BAD_REQUEST

    
    return make_response(jsonify({"rooms": rooms}))



# Use this route for POST request on /rooms
@app.route('/api/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    room_schema = RoomSchema()
    try: 
        room = room_schema.load(data)
        print(room)

    # Fix the exception handler
    except ValidationError as exec:
        return {
            'message' : "Validation errors", 'errors': exec.messages
        }, HTTPStatus.BAD_REQUEST
    result = room_schema.dump(room.create())
    return make_response(jsonify({"room": result }))


@app.route('/api/rooms/<id>', methods=['GET'])
def get_room_by_id(id):
    get_room = Room.query.get(id);
    room_schema = RoomSchema()
    try:
        room = room_schema.dump(get_room)
    except ValidationError as exec:
        return {
            'message' : "Validation errors", 'errors': exec.messages
        }, HTTPStatus.BAD_REQUEST

    return make_response(jsonify({ "room": room }))
