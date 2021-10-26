from flask import Flask, redirect, request
from os import urandom
from flask_mail import Mail
import json

# from signup import signup
from login import login
from products import products
from sellers import sellers
from upload import upload
from signup import signupUser_method, verify_otp
import stripe
import logging

import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.environ.get("STRIPE_API_KEY")

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

app = Flask(__name__, template_folder=".", static_folder = ".")
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
app.register_blueprint(login)
app.register_blueprint(products)
app.register_blueprint(sellers)
app.register_blueprint(upload)

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
  return return_status

@app.route('/verify', methods= ['POST'])
def verify_user():
  data = json.loads(request.data)
  username = data['username']
  otp = data['otp']
  print(otp, username)
  return verify_otp(otp, username)

YOUR_DOMAIN = 'http://localhost:3000/Checkout'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # TODO: replace this with the `price` of the product you want to sell
                    'price': 'price_1Jn26SSH89lyqSfk6QJGFobr',
                    'quantity': 1,
                },
            ],
            payment_method_types=[
              'card',
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '?success=true',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(debug=True)