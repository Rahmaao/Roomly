'''Creates Traits Model'''


# We first import app from app.py -- If you open app.py in the roomly root folder,
# you'll find that there's also an app variable. It is that variable that we have imported in here.
# The other imports are sql_alchemy modules to help us with our database CRUD operations
from app import app
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# initialize the db here
db = SQLAlchemy(app)

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


db.create_all()


class TraitsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Traits
        load_instance = True
        # When foriegn keys are implemented we add this
        # include_fk = True
        sqla_session = db.session
