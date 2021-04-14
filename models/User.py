from app import app
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


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


    # This is a Model method for creating user entries.
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


    # Add set password and checkpassword Model method

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

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