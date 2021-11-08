from ctypes import resize
import hashlib
from typing import Counter
from flask import Flask, redirect, request
from os import urandom
from flask.globals import session
from flask_mail import Mail
from flask_mail import Message
import json
import random
import gmpy2
import traceback
from flask import current_app

import sys
from errors import INVALID_AUTH_TOKEN, PERMISSION_DENIED
from products import products
from sellers import sellers
from upload import upload
from users import users
from profile import profile
import signup
import stripe
import logging
from random import randint
import db_helper

import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.environ.get("STRIPE_API_KEY")

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

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

app.register_blueprint(products)
app.register_blueprint(sellers)
app.register_blueprint(upload)
app.register_blueprint(users)
app.register_blueprint(profile)

@app.errorhandler(Exception)
def unhandled_exception(e):
    response = dict()
    error_message = traceback.format_exc()
    app.logger.error("Caught Exception: {}".format(error_message))
    response["errorMessage"] = error_message
    return response, 500

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = 'https://localhost:3000'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'
    return response

@app.route('/signup', methods= ['POST'])
def signupUser():
    return_status = signup.signupUser_method(mail)
    app.logger.info(return_status)
    return return_status

@app.route('/login', methods= ['POST'])
def checkCredentials():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    role = data['role']

    if(role == 'User' or role == 'Seller'):
      auth_token = db_helper.check_login_credentials(username, password, role)
      if auth_token:
        return 'true ' + auth_token
      else:
        return 'Username or Password is incorrect'

    admin_email = db_helper.check_admin_login_credentials(username, password)

    ###### SEND EMAIL ######
    otp = randint(000000,999999) 
    msg = Message('OTP',sender = 'amawon80@gmail.com', recipients = [admin_email])  

    db_helper.create_otp(username, otp)
    
    msg.body = str(otp)
    return_status = mail.send(msg)
    auth_token = db_helper.generateToken(data['username'])
    return "true " + auth_token

@app.route('/verify', methods= ['POST'])
def verify_user():
    data = json.loads(request.data)
    username = data['username']
    otp = data['otp']
    return str(db_helper.verify_otp(otp, username))

@app.route('/logout', methods= ['GET'])
def logout():
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    if not user:
        return INVALID_AUTH_TOKEN
    db_helper.generateToken(user['username'])

@app.route('/webhook', methods = ['POST'])
def webhook():
    ep_secret = "whsec_bmj0hLPIMpdyRROHzqUEDpiJlmvT2Pmb"
    #print (request.json)

    if request.json['type'] == 'payment_intent.succeeded':
        db_helper.fulfill_order(request.json['data']['object']['metadata']['order_id'])

    if request.json['type'] == 'payment_intent.created':
        print (request.json)


    return "YEY"

def getPublicKey():
    public_key = open('./public_key.pub', 'r', encoding='utf-8-sig').read()
    return public_key

def getPrivateKey():
    private_key = open('./private_key.pem', 'r', encoding='utf-8-sig').read()
    return private_key

def encrypt(m, d, n):
    c = pow(m, d, n)
    return c

@app.route('/get_certificate')
def return_certificate():
    try:
        f = json.loads(open('./myca.cert', 'r', encoding='utf-8-sig').read())
        private_key = gmpy2.mpz(getPrivateKey())
        public_key = gmpy2.mpz(getPublicKey())
        m = gmpy2.mpz(f['m'])
        return json.dumps({'enc_m': str(encrypt(m, private_key, public_key)), 'public_key': getPublicKey(), 'cert': True, 'enc_m_CA': f['enc_m']})
    except:
        return json.dumps({'cert': False})


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    if not user:
        return INVALID_AUTH_TOKEN
    if user['role'] != "User":
        return PERMISSION_DENIED
    try:
        order_id = hashlib.sha256(os.urandom(20)).hexdigest()[:30]
        products = Counter()
        for i in request.json:
            products[i] += 1
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": db_helper.get_product(i)["price_id"], 
                    "quantity": products[i]
                } 
                    for i in products
                ],
            payment_method_types=[
              'card',
            ],
            mode='payment',
            payment_intent_data = {"metadata":{'username':user['username'], 'order_id': order_id}},
            success_url="https://localhost:3000/Checkout?success=true",
            cancel_url="https://localhost:3000/Checkout?cancelled=false",
        )
    except Exception as e:
        print (e)
        return str(e)

    db_helper.create_order(order_id, products, user['username'])
    return checkout_session.url

if __name__ == '__main__':
    context = ('./localhost.pem', './localhost-key.pem')
    app.run(debug=True, ssl_context=context)