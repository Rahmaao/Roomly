from database import Hostel, HostelSchema, db, Room, RoomSchema
from flask_restful import reqparse, abort, Api, Resource
from app import app
from flask import jsonify, request
from controllers.factoryController import get_all, create_one, get_one, delete_one

api = Api(app)

class HostelList(Resource):
    """
    Resource for /api/hostel endpoint

    """
    def get(self):

        data = get_all('hostel')
        return {
            "hostels": data,
            "results": len(data)
        }
    
    def post(self):
        """
        Handles post requests to /api/hostel endpoint
        accepts name, price through json
        """
        # Parser helps us to clean the sent data.
        #  after initiliazing parser. Only arguments
        # added afterwards would be saved.

        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('price')

        data = parser.parse_args()
        hostel = create_one('hostel', data)

        return { "hostel" : hostel }

class SingleHostel(Resource):
    """
    Handles /api/hostel/<id> endpoint
    """

    def get(self, id):
        """
        Handles a get request returns a single hostel
        """
        hostel = get_one('hostel', id)
        return {
            "hostel" : hostel
        }

    def patch(self, id):

        """
        Handles patch requests to the end point. Updates hostel record.
        """
        # Parser helps us to clean the sent data.
        #  after initiliazing parser. Only arguments
        # added afterwards would be saved.

        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('price')

        # Save parsed data as dictionary
        data = parser.parse_args()

        # If the user ddin't send an argument in the data dictionary,
        # the value will be None


        hostel_schema = HostelSchema()
        hostel = Hostel.query.get_or_404(id)

        # This means the user actually sent name
        # Update the anem
        if data['name'] != None:
            hostel.name = data['name']
        
        if data['price'] != None:
            hostel.price = data['price']

        db.session.commit()

        hostel = hostel_schema.dump(hostel)

        return {"hostel" : hostel}

    def delete(self, id):
        return delete_one('hostel', id)

class RoomsOnHostel(Resource):
    """
    This resource handles requests to /api/hostels/<id>/rooms
    """
    def get(self, id):
        """
        Get all rooms with the id of the hostel on the endpoint
        """

        hostel = Hostel.query.get(id)

        if not hostel:
            return jsonify({
                'message': 'No hostel found with that id'
            })

        rooms = Room.query.filter_by(hostel=hostel)
        rooms = RoomSchema(many=True).dump(rooms)

        return jsonify({
            'rooms' : rooms
        })

    def post(self, id):
        
        """
        This create a room with the hostel field set to the hostel record with id
        """

        hostel = Hostel.query.get(id)
        # Parse relevant fields
        data = request.json
        room = RoomSchema().load(data)

        room.hostel = hostel
        room = RoomSchema().dump(room.create())

        return {
            'room': room
        }


api.add_resource(HostelList, '/api/hostels')
api.add_resource(SingleHostel, '/api/hostels/<id>')
api.add_resource(RoomsOnHostel, '/api/hostels/<id>/rooms')










