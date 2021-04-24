from flask import Flask, session
# from flask_jwt_extended import JWTManager```

app = Flask(__name__)
app.config.from_object('config.Config')

import database

from routes import hostelRoutes
from routes import authRoutes
from routes import viewRoutes
from routes import roomRoutes
from routes import userRoutes
from routes import traitRoutes
from routes import admin

# authors.index()


# import views
