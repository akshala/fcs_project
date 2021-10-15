from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from datetime import date
from os import urandom
import json
import time
from random import randint

import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

signup = Blueprint('signup',__name__)

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

@signup.route('/signup', methods= ['POST'])
def signupUser():
    data = json.loads(request.data)
    print(data)
    
    if(checkEmailExists(data['email'])):
        return 'Email already exists'

    if(checkUsernameExists(data['username'])):
        return 'Username already exists'

    dbCursor = db.cursor()
    userId = generateUID()
    
    sqlQuery = 'insert into user_details values (%s, %s, %s);'
    val = (userId, data['name'], data['email'])
    dbCursor.execute(sqlQuery, val)
    db.commit()

    sqlQuery = 'insert into login_credentials values (%s, %s, %s, %s);'
    val = (userId, data['username'], data['password'], data['username'])
    dbCursor.execute(sqlQuery, val)
    db.commit()

    dbCursor.close()
    return 'User registered successfully'