from flask import Flask
from os import urandom
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)


def create_app():
    app = Flask(__name__)
    app.secret_key = urandom(24)
    
    # from .auth import auth
    # from .main import main

    # app.register_blueprint(main)
    # app.register_blueprint(auth)
    

    return app