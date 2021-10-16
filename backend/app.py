from flask import Flask
from os import urandom
from flask_mail import Mail

# from signup import signup
from products import products
from sellers import sellers
from signup import signupUser_method, verify_otp

import logging

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

app = Flask(__name__)
app.secret_key = urandom(24)

app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465      
app.config["MAIL_USERNAME"] = 'amawon80@gmail.com'  
app.config['MAIL_PASSWORD'] = 'fcs_project80'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True 
app.config['MAIL_DEBUG'] = True 
app.config['MAIL_SUPPRESS_SEND'] = False
mail = Mail(app)  

# app.register_blueprint(signup)
app.register_blueprint(products)
app.register_blueprint(sellers)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'
    return response

@app.route('/signup', methods= ['POST'])
def signupUser():
  return_status = signupUser_method(mail)
  app.logger.info(return_status)
  return 'User registered successfully'

@app.route('/verify', methods= ['GET'])
def verify_user():
  return verify_otp()

if __name__ == 'main':
    create_app()
    app.run(debug=True)