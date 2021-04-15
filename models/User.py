from app import app
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from passlib.hash import pbkdf2_sha256 as sha256


# initialize the db here
db = SQLAlchemy(app)

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

# Create User model
db.create_all()

# 
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        # When foriegn keys are implemented we add this
        # include_fk = True