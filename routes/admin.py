from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database import Hostel, Room, User, Trait, db
from app import app
from app import jwt
from flask_jwt_extended import jwt_required


admin = Admin(app, name='Roomly-Admin', template_mode='bootstrap4', url='/admin')

# Add Administrative views here
admin.add_view(ModelView(Hostel, db.session))
admin.add_view(ModelView(Room, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Trait, db.session))

