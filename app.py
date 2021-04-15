from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Config')

from routes import authRoutes
from routes import viewRoutes
from routes import roomRoutes
from routes import userRoutes

# authors.index()


# import views
