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
import errors
import input_validation_helper

CAPTCHA_SECRET_KEY = os.environ.get("CAPTCHA_SECRET_KEY")


db = mysql.connector.connect(
  host="localhost",
  user=os.environ.get("USER_DB"),
  passwd=os.environ.get("PASSWORD_DB"),
  database=os.environ.get("DB")
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
        return errors.CAPTCHA_FAILED

    if not input_validation_helper.check_email_valid(data['email']):
        return errors.INVALID_EMAIL

    if(db_helper.check_email_exists(data['email'])):
        return errors.EMAIL_EXISTS

    if(db_helper.check_username_exists(data['username'])):
        return errors.USERNAME_EXISTS

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
    return_status = mail.send(msg)
    dbCursor.close()
    return errors.SUCCESS