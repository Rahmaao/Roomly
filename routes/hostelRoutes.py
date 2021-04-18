from database import Hostel, HostelSchema, db
from flask_restful import reqparse, abort, Api, Resource
from app import app

api = Api(app)

class HostelList(Resource):
    def get(self):
        
        # Query hostels
        hostels = Hostel.query.all()
        hostel_schema = HostelSchema(many=True)

        hostels = hostel_schema.dump(hostels)

        return {
            "hostels": hostels,
            "results": len(hostels)
        }
    
    def post(self):

        hostel_schema = HostelSchema()
        
        # Parser helps us to clean the sent data.
        #  after initiliazing parser. Only arguments
        # added afterwards would be saved.

        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('price')

        # Save parsed data as dictionary
        data = parser.parse_args()

        # Deserialize(convert to object) data dictionary
        hostel = hostel_schema.load(data)

        # Serialize(convert to json) created record
        hostel = hostel_schema.dump(hostel.create())

        return { "hostel" : hostel }

class SingleHostel(Resource):

    def get(self, id):


        hostel_schema = HostelSchema()
        hostel = Hostel.query.get(id)

        hostel = hostel_schema.dump(hostel)

        return {
            "hostel" : hostel
        }

    def patch(self, id):
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
        hostel = Hostel.query.get(id)

    # Test for result
        if not hostel:
            return {
                "No hostel with that ID"
            }

        # This means the user actually sent name
        # Update the anem
        if data['name'] != None:
            hostel.name = data['name']
        
        if data['price'] != None:
            hostel.price = data['price']

        db.session.commit()

        return hostel_schema.dump(hostel)

    def delete(self, id):

        # Query hostel
        # hostel_schema = HostelSchema()
        hostel = Hostel.query.get(id)
        # hostel = hostel_schema.dump(ho)

        # Check if hostel exits
        if not hostel:
            return {
                "No hostel with that ID"
            }

        # Delete hostel record

        db.session.delete(hostel)
        db.session.commit()

        return '', 204


api.add_resource(HostelList, '/api/hostels')
api.add_resource(SingleHostel, '/api/hostels/<id>')










