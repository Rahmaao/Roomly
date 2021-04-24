from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database import Hostel, Room, User, Trait, db
from app import app
from flask import session, redirect, request, url_for
from routes.authRoutes import jwt
from flask_jwt_extended import jwt_required

class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return session.get('user') == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('index'))


admin = Admin(app, name='Roomly-Admin', template_mode='bootstrap4', index_view=AdminView(Hostel, db.session, url='/admin', endpoint='admin')) 

# Add Administrative views here
# admin.add_view(ModelView(Hostel, db.session))
admin.add_view(ModelView(Room, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Trait, db.session))

