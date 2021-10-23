from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from datetime import date
from os import urandom
import json
import time
from random import randint
import sys
from flask_mail import Message
from datetime import datetime

# signup = Blueprint('signup',__name__) 

import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

otp = randint(000000,999999) 

import mysql.connector
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

def checkUsernameExists(username):
    
    dbCursor = db.cursor()
    sqlQuery = 'select * from login_credentials where username = %s;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if(len(res) > 0):
        return True
    return False

def checkEmailExists(email):

    dbCursor = db.cursor()
    sqlQuery = 'select * from user_details where email = %s;'
    val = (email, )
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if(len(res) > 0):
        return True
    return False

# @signup.route('/signup', methods= ['POST'])
def signupUser_method(mail):
    data = json.loads(request.data)
    print(data)
    
    if(checkEmailExists(data['email'])):
        return 'Email already exists'

    if(checkUsernameExists(data['username'])):
        return 'Username already exists'

    dbCursor = db.cursor()
    userId = generateUID()
    
    sqlQuery = 'insert into user_details values (%s, %s, %s, %s, %s);'
    val = (userId, data['username'], data['name'], data['email'], False)
    dbCursor.execute(sqlQuery, val)
    db.commit()

    sqlQuery = 'insert into login_credentials values (%s, %s, %s, %s);'
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
    return return_status

def verify_otp(user_otp, username):

    dbCursor = db.cursor()
    sqlQuery = 'select otp from otp_table where username=(%s);'
    val = (username)
    dbCursor.execute(sqlQuery, val)
    result = dbCursor.fetchAll()
    otp = result[0]

    if otp == user_otp:
        return True
    dbCursor.close()
    return False