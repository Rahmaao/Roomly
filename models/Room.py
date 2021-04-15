'''Creates Rooms Model'''


# We first import app from app.py -- If you open app.py in the roomly root folder,
# you'll find that there's also an app variable. It is that variable that we have imported in here.
# The other imports are sql_alchemy modules to help us with our database CRUD operations
from app import app
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# initialize the db here
db = SQLAlchemy(app)


# Initialize Room table
class Room(db.Model):

    # Set table name
    __tablename__='rooms'
    # Define Room columns

    id = db.Column(
        db.Integer, 
        primary_key=True
        )

    name = db.Column(
        db.String(4), 
        unique=True, 
        nullable=False
        )

    available = db.Column(
        db.Boolean
        )

    bathroom = db.Column(
        db.Boolean
        )

    bedspace = db.Column(
        db.Integer
        )
    
    # Many to One Relationship to be implemented
    # occupants = db.relationship('User', backref='room', lazy=True)

    # hostel = db.relationship('')
    
    # Create method
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_id(self, id):
        return self.query.get(id)

    @classmethod
    def delete_by_id(self, id):

        # Find record by id. Delete record 
        record = self.find_by_id(id)
        db.session.delete(record)
        db.session.commit()
        return self

    @classmethod
    def update_by_id(self, id, fields):

        # We don't have to check for id. 
        # That was done before we called this method. 
        # Just find the record
        record = self.query.filter_by(id = id).first()

        # Iterate over values in fields dict, check if there are in
        # class atrributes (i.e part of our table columns)
        # Change as appropriate
        print('here')
        for field in [*fields]:
        # try: 
            print(f'Old record {record.field}')
            record.field = fields[field]
            print(f'New record {record.field}')

        # except AttributeError as err:
        #     return err
        db.session.commit()
        return record
        # return result
    
    #Initialization method
    def __init__(self, name, available = True, bathroom = False, bedspace = 3):
        self.name = name
        self.available = available 
        self.bathroom = bathroom
        self.bedspace = bedspace 

    
    # This is in the documentation too. I guess it's how the Model
    # describes itself.
    def __repr__(self):
        return '<Room %r>'%self.name

#create above model
db.create_all()

# Omo. I no too get this one. Just copy and past and edit to
# suit the Model you're using. It's very important
class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        # When foriegn keys are implemented we add this
        # include_fk = True
        sqla_session = db.session
