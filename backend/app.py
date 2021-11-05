from flask import Flask, redirect, request
from os import urandom
from flask_mail import Mail
from flask_mail import Message
import json

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
from datetime import datetime
import db_helper

import os
from dotenv import load_dotenv

import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

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

# app.register_blueprint(signup)
# app.register_blueprint(login)
app.register_blueprint(products)
app.register_blueprint(sellers)
app.register_blueprint(upload)
app.register_blueprint(users)
app.register_blueprint(profile)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'
    return response

@app.route('/signup', methods= ['POST'])
def signupUser():
    print('here')
    return_status = signup.signupUser_method(mail)
    app.logger.info(return_status)
    return return_status

@app.route('/login', methods= ['POST'])
def checkCredentials():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    role = data['role']

    print(username, password)

    dbCursor = db.cursor()
    if(role == 'User' or role == 'Seller'):
      auth_token = db_helper.check_login_credentials(username, password, role)
      if auth_token:
        return 'true ' + auth_token
      else:
        return 'Username or Password is incorrect'

    sqlQuery = 'Select * from login_credentials_admin where username = %s and  password = %s;'
    val = (username, password)
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if(len(res) == 0):
      dbCursor.close()
      return "Username or password is incorrect"

    sqlQuery = 'select email from admin_details where username = %s'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if(len(res) == 0):
        dbCursor.close()
        return False
    admin_email = res[0][0]

    ###### SEND EMAIL ######
    otp = randint(000000,999999) 
    msg = Message('OTP',sender = 'amawon80@gmail.com', recipients = [admin_email])  
    
    sqlQuery = 'insert into otp_table values (%s, %s, %s);'
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    val = (data['username'], otp, formatted_date)
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()
    
    msg.body = str(otp)  
    print(msg, file=sys.stderr)
    return_status = mail.send(msg)
    print('return_status={}'.format(return_status))
    return "true "

@app.route('/verify', methods= ['POST'])
def verify_user():
    data = json.loads(request.data)
    username = data['username']
    otp = data['otp']
    return str(db_helper.verify_otp(otp, username))

YOUR_DOMAIN = 'http://localhost:3000/Checkout'

# @app.route('successfulPayment', methods=['GET'])
# def successfulPayment():
    


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    if not user:
        return INVALID_AUTH_TOKEN
    if user['role'] != "User":
        return PERMISSION_DENIED
    try:
        products = [db_helper.get_product(i) for i in request.json]
        print (products)
        checkout_session = stripe.checkout.Session.create(
            line_items=[{"price": i["price_id"], "quantity": 1} for i in products],
            # [
            #     {
            #         # TODO: replace this with the `price` of the product you want to sell
            #         'price': 'price_1JpD6wSH89lyqSfktXWxLHmG',
            #         'quantity': 1,
            #     },
            # ],
            payment_method_types=[
              'card',
            ],
            mode='payment',
            success_url="http://localhost:5000/successfulPayment",
            cancel_url="https://localhost:3000/Checkout",
        )
    except Exception as e:
        print (e)
        return str(e)

    return checkout_session.url

if __name__ == '__main__':
    app.run(debug=True)