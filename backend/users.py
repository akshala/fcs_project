from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json
from os import urandom

users = Blueprint('users',__name__)

import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

@users.route("/users")
def get_users():
    return json.dumps(get_user(), separators=(',', ':'))


@users.route("/delete_user",  methods= ['POST'])
def delete_users():
    data = json.loads(request.data)
    username = data['username']
    print(username)
    dbCursor = db.cursor()

    sqlQuery = 'delete from user_details where username = %s ;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    db.commit()

    sqlQuery = 'delete from login_credentials where username = %s ;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    db.commit()

    dbCursor.close()
    return "True"

def get_user():
    dbCursor = db.cursor()
    sqlQuery = 'Select * from user_details;'
    dbCursor.execute(sqlQuery)
    res = dbCursor.fetchall() # List of tuples
    users = []
    for elt in res:
      print(elt)
      temp_dict = {}
      temp_dict['username'] = elt[1]
      temp_dict['name'] = elt[2]
      temp_dict['email'] = elt[3]
      temp_dict['verified'] = elt[4]
      users.append(temp_dict)
    print(users)
    dbCursor.close()
    print("Done")
    return users