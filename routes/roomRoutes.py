''''This handles all requests to /rooms route.
imports Rooms, RoomSchema model
'''

from database import Room, RoomSchema, db, User, UserSchema, Hostel, HostelSchema
from flask import make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import *
from flask_restful import reqparse, abort, Api, Resource

from app import app

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
            "results" : len(rooms)
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

        # Parse relevant fields
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('hostel')
        parser.add_argument('bathroom')
        parser.add_argument('bedspace')

        # Save as dictionary
        data = parser.parse_args()
        
        # Query room
        room = Room.query.get(id)

        # Check if fields are actually part of the request.

        # If field is not NOne, update record
        if data['name'] != None:
            room.name = data['name']

        if data['bathroom'] != None:
            room.bathroom = data['bathroom']

        if data['bedspace'] != None:
            room.bedspace = data['bedspace']

        if data['hostel'] != None:
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

api.add_resource(RoomList, '/api/rooms')
api.add_resource(SingleRoom, '/api/rooms/<id>')

# # Use the route for  GET request on /rooms
# @app.route('/api/rooms', methods=['GET'])
# def get_rooms():

#     get_rooms = Room.query.all()
#     room_schema = RoomSchema(many=True)
#     try:
#         rooms = room_schema.dump(get_rooms)
#     except ValidationError as exec:
#         return {
#             'message' : "Validation errors", 'errors': exec.messages
#         }, HTTPStatus.BAD_REQUEST
    
#     return make_response(jsonify({"rooms": rooms, "results": len(rooms)}))

# # Use this route for POST request on /rooms
# @app.route('/api/rooms', methods=['POST'])
# def create_room():
#     #To be refactored
#     hostel_schema = HostelSchema()
#     room_schema = RoomSchema()
#     # get json data from request
#     data = request.json

#     get_hostel = Hostel.query.get(data['hostel'])  

#     del data['hostel']
#     new_room = room_schema.load(data)


#     # data['hostel'] = get_hostel
#     # new_room = Room(name=data['name'], hostel = get_hostel)

#     hostel = hostel_schema.dump(get_hostel)

#     room = room_schema.dump(new_room)

#     room['hostel'] = hostel;

#     new_room = room_schema.load(room)




#     result = room_schema.dump(new_room.create())

#     # try: 
#     #     room = room_schema.load(data)
#     # except ValidationError as exec:
#     #     return {
#     #         'message' : "Validation errors", 'errors': exec.messages
#     #     }, HTTPStatus.BAD_REQUEST
#     # result = room_schema.dump(room.create())

#     return make_response(jsonify({"room": result}))


# @app.route('/api/rooms/<id>', methods=['GET'])
# def get_room_by_id(id):

#     # Query a room
#     get_room = Room.query.get(id)
#     result = room_schema.dump(get_room)

#     # Test for result
#     if not result:
#         return make_response(jsonify({
#             "message": "No room with that id."
#         }))

#     # Return room
#     return room_schema.dump(get_room)

# @app.route('/api/rooms/<id>', methods=['DELETE'])
# def delete_room_by_id(id):

#     # Query room data
#     get_room = Room.query.get(id)
#     room = room_schema.dump(get_room)

#     # If empty result, room with ID doesn't exist
#     if not room:
#         return make_response(jsonify({ 'message' : 
#         'Room with this ID does not exist'}))
        
#     db.session.delete(get_room)
#     db.session.commit()

#     # Send response
#     return '', 204




# @app.route('/api/rooms/<id>', methods=['PATCH'])
# def update_room_by_id(id):

#     # The difference between a PATCH and PUT
#     # request is that PATCH modifies entry. Meanwhile
#     # PUT actualaly clears the old entry and reenters the values

#     # Get json data from response

#     data = request.json
#     get_room = Room.query.get(id)

#     # Test for result
#     if not get_room:
#         return make_response(jsonify({
#             "message": "No room with that id."
#         }))


#     if 'name' in data:
#         get_room.name = data['name']
    
#     if 'available' in data:
#         get_room.available = data['available']

#     if 'bathroom' in data:
#         get_room.bathroom = data['bathroom']
    
#     if 'bedspace' in data:
#         get_room.bedspace = data['bedspace']

#     db.session.commit()

#     return room_schema.dump(get_room)
    



# # I'm not sure these routes work just yet
# # Route to assign users to room
# @app.route('/api/rooms/<id>/occupants', methods=['GET'])
# def get_users_by_room(id):

#     # Make a request to to api/users/
#     get_users = User.query.filter_by(room_id = id)
#     user_schema = UserSchema(many=True)    

#     users = user_schema.dump(get_rooms)

#     # filter by room_id

#     # Nested routes

#     # Get room
#     # Return all the occupants of the room
#     return make_response({ "message": "success",
#                             "users": users,
#                             "results": len(users) }, 200)


# @app.route('/api/rooms/<id>/users', methods=['POST'])
# def add_user_to_room(id):

#     # Nested routes Really?

#     # Add room.id = id to request.data
#     data = request.json
#     data['room'] = id

#     # Send request to /users/
#     user_schema = UserSchema()
#     user = user_schema.load(data)
#     result = user_schema.dump(user.create())

#     # Get room
#     # Get user id
    
#     # Add id to the occupant field
#     db.session.commi()

#     return make_response({"message":"success", "user": result})

