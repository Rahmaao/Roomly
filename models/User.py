from app import app
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

# initialize the db here
db = SQLAlchemy(app)

# Initialize User table
class User(db.Model):
    # Define User colums
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(125), unique=True)
    username = db.Column(db.String(125), unique=True)
    password = db.Column(db.String(125))


    # This is a Model method for creating user entries.
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>'%self.username

db.create_all()

class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session
    
    id = fields.Number(dump_only=True)
    email = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
