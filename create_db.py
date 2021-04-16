from app import app
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from passlib.hash import pbkdf2_sha256 as sha256


# initialize the db here
db = SQLAlchemy(app)


class Hostel(db.Model):

    # Set table name
    __tablename__ = 'hostels'


    # Set table column
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(255),
        unique = True,
        nullable = False
    )

    price = db.Column(
        db.Integer
    )

    # rooms = db.relationship(
    #     'Room', 
    #     lazy='select',
    #     backref = db.backref('hostel', lazy='joined'))

# Initialize Room table
class Room(db.Model):

    # Set table name
    __tablename__= 'rooms'
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
    
    # hostel_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey('hostels.id'),
    #     nullable=True
    #     )
    
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

# Initialize User table
class User(db.Model):

    # set table name
    __tablename__ = 'users'

    # Define User colums
    id = db.Column(
        db.Integer, 
        primary_key=True
        )
    email = db.Column(
        db.String(125), 
        unique=True
        )
    username = db.Column(
        db.String(125), 
        unique=True
        )
    password = db.Column(
        db.String(125)
        )
    isAdmin = db.Column(
        db.Boolean
        )


    # This is a Model method for creating user entries.
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_username(self, username):
        return self.query.filter_by(username = username).first()

    # To implement set password method-- encryption

    @staticmethod
    def check_password(candidate_password, password):
        return candidate_password == password


    # Add set password and checkpassword Model method

    def __init__(self, email, username, password, isAdmin = False):
        self.email = email
        self.username = username
        self.password = password
        self.isAdmin = isAdmin

    def __repr__(self):
        return '<User %r>'%self.username


class Traits(db.Model):

    # Set table name
    __tablename__='traits'
    # Define Room columns

    id = db.Column(
        db.Integer, 
        primary_key=True
        )

    traits = db.Column(
        db.String(255), 
        unique=True, 
        nullable=False
        )

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


    def __init__(self, traits):
        self.traits = traits


    def __repr__(self):
        return '<Traits %r>'%self.traits


# Create User model
db.create_all()

class HostelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Hostel
        load_instance = True
        # include_fk = True
        sqla_session = db.session

# 
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session


# Omo. I no too get this one. Just copy and past and edit to
# suit the Model you're using. It's very important

class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        # When foriegn keys are implemented we add this
        # include_fk = True
        sqla_session = db.session


class TraitsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Traits
        load_instance = True
        # When foriegn keys are implemented we add this
        # include_fk = True
        sqla_session = db.session
