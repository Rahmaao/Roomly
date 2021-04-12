from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.config.from_object('config.Config')

# Intialize MySQL
mysql = MySQL(app)