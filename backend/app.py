from flask import Flask
from os import urandom

from signup import signup
from products import products

import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

app = Flask(__name__)
app.secret_key = urandom(24)


app.register_blueprint(signup)
app.register_blueprint(products)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'
    return response

if __name__ == 'main':
    create_app()
    app.run(debug=True)