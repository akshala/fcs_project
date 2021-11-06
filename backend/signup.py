from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from datetime import date
from os import urandom
import json
import time
from random import randint
import sys
from flask_mail import Message
from datetime import datetime
import db_helper
import requests
import mysql.connector
import os

CAPTCHA_SECRET_KEY = os.environ.get("CAPTCHA_SECRET_KEY")


db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

def generateUID(length=12):
    d = [str(i) for i in range(10)]
    d = d + [chr(ord('a') + i) for i in range(26) ]
    d = d + [chr(ord('A') + i) for i in range(26) ]
    uid = ""
    tm = int(time.time())
    while tm>0:
        rem = tm % len(d)
        tm//=len(d)
        uid = uid + d[rem]
    
    while len(uid) < length:
        uid = uid + d[randint(0,len(d)-1)]

    return uid

def signupUser_method(mail):
    otp = randint(000000,999999) 
    data = json.loads(request.data)

    captcha_data = { "secret": CAPTCHA_SECRET_KEY, "response": data['captcha']}

    x = requests.post("https://www.google.com/recaptcha/api/siteverify", data = captcha_data)

    if x.json()['success'] != True:
        return "Captcha Failed"

    if(db_helper.check_email_exists(data['email'])):
        return 'Email already exists'

    if(db_helper.check_username_exists(data['username'])):
        return 'Username already exists'

    dbCursor = db.cursor()
    userId = generateUID()

    if(data['type'] == 'User'):
        sqlQuery = 'insert into user_details values (%s, %s, %s, %s, %s);'
        val = (userId, data['username'], data['name'], data['email'], False)
    else:
        sqlQuery = 'insert into seller_details values (%s, %s, %s, %s, %s, %s);'
        val = (userId, data['username'], data['name'], data['email'], False, False)
    
    dbCursor.execute(sqlQuery, val)
    db.commit()

    if(data['type'] == 'User'):
        sqlQuery = 'insert into login_credentials values (%s, %s, %s, %s);'
    else:
        sqlQuery = 'insert into login_credentials_seller values (%s, %s, %s, %s);'
    
    val = (userId, data['username'], data['password'], data['username'])
    dbCursor.execute(sqlQuery, val)
    db.commit()

    sqlQuery = 'insert into otp_table values (%s, %s, %s);'
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    val = (data['username'], otp, formatted_date)
    dbCursor.execute(sqlQuery, val)
    db.commit()

    msg = Message('OTP',sender = 'amawon80@gmail.com', recipients = [data['email']])  
    msg.body = str(otp)  
    print(msg, file=sys.stderr)
    return_status = mail.send(msg)
    print('return_status={}'.format(return_status))
    dbCursor.close()
    return 'User registered successfully'

def verify_otp(user_otp, username):
    if db_helper.verify_otp(user_otp, username):
        return "True"
    return "False"