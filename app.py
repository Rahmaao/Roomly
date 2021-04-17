from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Config')

import database

from routes import authRoutes
from routes import viewRoutes
from routes import roomRoutes
from routes import userRoutes
from routes import traitRoutes

# authors.index()


# import views
