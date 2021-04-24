from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import app

db = SQLAlchemy(app)


class Hostel(db.Model):

    __tablename__ = 'hostel'

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    name = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )

    price = db.Column(
        db.Integer,
        nullable=False
    )

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Hostel {self.name}>'

class Room(db.Model):

    __tablename__ = 'room'

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
        db.ForeignKey('hostel.id')
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


# Table of users and traits
user_trait = db.Table('user_trait',
        db.Column('trait_id', db.Integer, db.ForeignKey('trait.id'), primary_key=True),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
        )


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    username = db.Column(
        db.String(255),

    )

    isAdmin = db.Column(
        db.Boolean,
        default = False
    )

    email = db.Column(
        db.String(255)
    )
    password = db.Column(
        db.String(255)
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey('room.id')
    )

    room = db.relationship(
        'Room', backref = 'occupants'
    )

    traits = db.relationship('Trait', secondary=user_trait, lazy='joined',
    backref=db.backref('users', lazy=True))


    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<User {self.username}>'


class Trait(db.Model):

    __tablename__: 'trait'

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    trait = db.Column(
        db.String(255),
        nullable=False
    )
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Triat {self.trait}>'
# db.create_all()

class TraitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Trait
        load_instance = True
        sqla_session = db.session


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_fk = True

    traits = fields.Nested(TraitSchema, many=True)



class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        sqla_session = db.session

    occupants = fields.Nested(UserSchema, many = True, only=["username", "id"])


# On the reference Schema, you'll speciffy the backref field like so.
class HostelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model= Hostel
        load_instance = True
        sqla_session = db.session

    rooms = fields.Nested(RoomSchema, many=True)