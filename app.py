from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.config.from_object('config.Config')

# Intialize MySQL
mysql = MySQL(app)

import views

# http://localhost:5000/main - this will be the logout page


