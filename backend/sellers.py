from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json
from os import urandom
import db_helper

sellers = Blueprint('sellers',__name__)

import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

@sellers.route("/sellers")
def get_sellers():
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    if not user:
        return []
    if user['role'] != "Admin":
        return []
    return json.dumps(get_sellers_helper(), separators=(',', ':'))

@sellers.route("/approve_seller",  methods= ['POST'])
def approve_seller():
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    if not user:
        return []
    if user['role'] != "Admin":
        return []

    data = json.loads(request.data)
    username = data['username']
    print(username)
    dbCursor = db.cursor()
    sqlQuery = 'update seller_details set approved = true where username = %s ;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()
    return "True"

@sellers.route("/delete_seller",  methods= ['POST'])
def delete_seller():
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    print('get seller', user)
    if not user:
        return []
    if user['role'] != "Admin":
        return []
        
    data = json.loads(request.data)
    username = data['username']
    print(username)
    dbCursor = db.cursor()

    sqlQuery = 'delete from seller_details where username = %s ;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    db.commit()

    sqlQuery = 'delete from login_credentials_seller where username = %s ;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    db.commit()

    dbCursor.close()
    return "True"

def get_sellers_helper():
    dbCursor = db.cursor()
    sqlQuery = 'Select * from seller_details;'
    dbCursor.execute(sqlQuery)
    res = dbCursor.fetchall() # List of tuples
    seller = []
    print(res)
    for elt in res:
      print(elt)
      temp_dict = {}
      temp_dict['username'] = elt[1]
      temp_dict['name'] = elt[2]
      temp_dict['email'] = elt[3]
      temp_dict['verified'] = elt[4]
      temp_dict['approved'] = elt[5]
      seller.append(temp_dict)
    print(seller)
    dbCursor.close()
    return seller