from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from . import db

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

@signup.route('/signup')
def checkUsernameValid():
    dbCursor = db.cursor()
    sqlQuery = 'Select * from login_credentials where username = %s'
    val = ('tt',) #(session['username'])
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if(len(res) > 0):
        return 'False'
    return 'True'

def checkEmailValid():
	dbCursor = db.cursor()
    sqlQuery = 'Select * from user_details where email = %s'
    val = ('tt',) #(session['email'])
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if(len(res) > 0):
        return 'False'
    return 'True'

def pushUserData():
	dbCursor = db.cursor()
	userId = generateUID()
    
    sqlQuery = 'insert into user_details values (%p, %p, %p)'
    val = (userId, session['name'], session['email'])
    dbCursor.execute(sqlQuery, val)
    db.commit()

    sqlQuery = 'insert into login_credentials values (%p, %p, %p, %p)'
    val = (userId, session['username'], session['password'], session['salt'])
    dbCursor.execute(sqlQuery, val)
    db.commit()

    dbCursor.close()