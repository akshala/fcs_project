from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json
from os import urandom


import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

login = Blueprint('login',__name__)

@login.route('/login', methods= ['POST'])
def checkCredentials():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']

    print(username, password)

    dbCursor = db.cursor()
    if(data['type'] == 'User'):
      sqlQuery = 'Select * from user_details u, login_credentials l where u.username = %s and u.username = l.username and u.verified = true and l.password = %s;'
    elif(data['type'] == 'Seller'):
      sqlQuery = 'Select * from seller_details u, login_credentials_seller l where u.username = %s and u.username = l.username and u.verified = true and l.password = %s and u.approved = true;'
    else:
      #### DO FOR ADMIN ####
      sqlQuery = 'Select * from user_details u, login_credentials l where u.username = %s and u.username = l.username and u.verified = true and l.password = %s;'
    val = (username, password)
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()

    print(res)
    
    if len(res) == 0:
    	return "False"
    return "True" 
