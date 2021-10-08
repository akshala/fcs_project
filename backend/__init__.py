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
    
    from .signup import signup
    app.register_blueprint(signup)
    
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=updateDues, trigger="interval", seconds=5)
    # scheduler.start()

    return app