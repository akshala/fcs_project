from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from . import db

login = Blueprint('login',__name__)

login.route('/checkCredentials')

def checkCredentials():

	dbCursor = db.cursor()
    sqlQuery = 'Select * from user_details where username = %s and password = %s'
    val = ('tt', 'tt2') #(session['email'])
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if len(res) == 0:
    	return 'False'
    return 'True'
