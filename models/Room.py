'''Creates Rooms Model'''


# We first import app from app.py -- If you open app.py in the roomly root folder,
# you'll find that there's also an app variable. It is that variable that we have imported in here.
# The other imports are sql_alchemy modules to help us with our database CRUD operations
from app import app
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

# initialize the db here
db = SQLAlchemy(app)


# Initialize Room table
class Room(db.Model):
    # Define Room columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    available = db.Column(db.Boolean)
    bathroom = db.Column(db.Boolean)
    bedspace = db.Column(db.Integer)
    
    # Many to One Relationship to be implemented
    # occupants = db.relationship('User', backref='room', lazy=True)

    # hostel = db.relationship('')
    # Create method
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
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
# suit the Model you're using.
class RoomSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Room
        sqla_session = db.session

    id = fields.Number(dump_only = True)
    name = fields.String(required= True)
    available = fields.Boolean()
    bathroom = fields.Boolean()
    bedspace = fields.Number()
