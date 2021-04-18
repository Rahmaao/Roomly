from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import app

db = SQLAlchemy(app)

class Hostel(db.Model):

    __tablename__ = 'hostels'

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    name = db.Column(
        db.String(40),
        unique=True
    )

    price = db.Column(
        db.Integer
    )

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Hostel {self.name}'

class Room(db.Model):

    __tablename__ = 'rooms'

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    name = db.Column(
        db.String(5),
        nullable = False
    )

    bathroom = db.Column(
        db.Boolean,
        default= False
    )

    bedspace = db.Column(
        db.Integer,
        default = 3
    )

    hostel_id = db.Column(
        db.Integer,
        db.ForeignKey('hostels.id')
    )

    # The idea is that we'll be able to specify the hostel
    # when we are creating a room record. Instead of
    # db.Column, we use db.relationship. Then we put the *class name*(not table name)
    # of the reference record. backref(specify name of the field) will create a field 
    # on the reference record,
    # which will be a list of all records that have a relationship with one specific
    # hostel record.
    hostel = db.relationship(
        "Hostel", 
        backref="rooms"
    )

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Room {self.name}>'


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    name = db.Column(
        db.String(255),

    )

    email = db.Column(
        db.String(255)
    )
    password = db.Column(
        db.String(255)
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey('rooms.id')
    )

    room = db.relationship(
        'Room', backref = 'occupants'
    )


    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Room {self.name}>'


# class Trait(db.Model):

#     __tablename__: 'traits'

#     id = db.Column(
#         db.Integer,
#         primary_key = True
#     )

#     name = db.Column(
#         db.String(255)
#     )

#     trait_group = db.Relationship('User', backref='traits')

db.create_all()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_fk = True



class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        sqla_session = db.session
        include_fk = True

    occupants = fields.Nested(UserSchema, many = True, only=["name", "id"])


# On the reference Schema, you'll speciffy the backref field like so.
class HostelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model= Hostel
        load_instance = True
        sqla_session = db.session

    rooms = fields.Nested(RoomSchema, many=True)