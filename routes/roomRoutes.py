''''This handles all requests to /rooms route.
imports Rooms, RoomSchema model
'''

from database import Room, RoomSchema, db, User, UserSchema, Hostel, HostelSchema
from flask import make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import *
from flask_restful import reqparse, abort, Api, Resource
from flask_jwt_extended import jwt_required, current_user
from app import app
from routes.authRoutes import jwt

api = Api(app)

# db = SQLAlchemy(app)



room_schema = RoomSchema()


class RoomList(Resource):
    def get(self):

        # Query rooms
        rooms = Room.query.all()
        room_schema = RoomSchema(many=True)

        rooms = room_schema.dump(rooms)
        return {
            "rooms" : rooms,
            "results" : len(rooms),
        }

    def post(self):

        # Parse relevant fields
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('hostel')
        parser.add_argument('bathroom')
        parser.add_argument('bedspace')

        # Save as dictionary
        data = parser.parse_args()
        room_schema = RoomSchema()

        # 
        # Check iF some fields are present, since they can be ignored,
        # and set to the model default

        if data['bathroom'] == None:
            del data['bathroom']

        if data['bedspace'] == None:
            del data['bedspace']
            
        # We are implementing a many-to-one relationship on Room. 
        # For some reason, parsing 'hostel' field
        # With the json won't be deserialized properly
        # with room_schema.load(). So, we get the 
        #  Deserialized data of the 'hostel' and save in
        # hostel. We then delete the 'hostel' field from
        # the data dictionary. We deserialize the data
        # dictionary--(convert to a Room object) and save in room. 
        # With both the room (which currently has no 'hostel' field),
        # and hostel(which we queried first). We then set the 'hostel'
        # field on room to the hostel. Finally, we create the record,
        # and serialize the room and save the result in room_json
        #  Phew!


        # Find the room with stated id.
        hostel = Hostel.query.get(data['hostel']);

        del data['hostel']

        # Create room without hostel field.
        room = room_schema.load(data)

        # Add hostel field
        room.hostel = hostel

        # Create and serialize new room
        room = room_schema.dump(room.create())


        return {'room': room }


class SingleRoom(Resource):
    def get(self, id):

        room_schema = RoomSchema()
        room = Room.query.get(id)

        if not room:
            return {
                "No room with that ID"
            }

        room = room_schema.dump(room)

        return {
            "room" : room
        }

    def patch(self, id):
        data = request.json
        
        # Query room
        room = Room.query.get(id)

        # Check if fields are actually part of the request.
        if 'name' in data:
            room.name = data['name']

        if 'bathroom' in data:
            room.bathroom = data['bathroom']

        if 'bedspace' in data:
            room.bedspace = data['bedspace']

        if 'hostel' in data:
            # Query hostel
            hostel = Hostel.query.get(data['hostel']);
            room.hostel = hostel

        # Commit changes
        db.session.commit()

        room = room_schema.dump(room)

        return {
            "room" : room
        }

    def delete(self, id):

        room = Room.query.get(id)

        if not room:
            return {
                "No room with that ID"
            }

        # Delete room record
        db.session.delete(room)
        db.session.commit()

        return '', 204

class UsersOnRoom(Resource):
    """
    This resource handles requests to /api/rooms/<id>/occupants
    """
    def get(self,id):
        "Get all users with the room id"

        # room = Hostel.
        users = User.query.filter_by(room_id=id)
        print(users)
        users = UserSchema(many=True).dump(users)

        return jsonify({
            "users" : users
        })
    def post(self, id):
        """
        This assigns a user to a room.
        """
        room = Room.query.get(id)
        data = request.json
        user = User.query.get(data['occupant'])
        room.occupants.append(user)
    
        db.session.commit()

        room = RoomSchema().dump(room)

        return {
            "room" : room
        }



api.add_resource(RoomList, '/api/rooms')
api.add_resource(SingleRoom, '/api/rooms/<id>')
api.add_resource(UsersOnRoom, '/api/rooms/<id>/occupants')
