from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json
from os import urandom

sellers = Blueprint('sellers',__name__)

seller = [
      {
        'id': 0,
        'name': "A",
        'description': "Groceries",
      },
      {
        'id': 1,
        'name': "B",
        'description': "Clothes",
      },
      {
        'id': 2,
        'name': "C",
        'description': "Electronics",
      }
  ]

import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

@sellers.route("/sellers")
def get_sellers():
    return json.dumps(get_sellers(), separators=(',', ':'))


@sellers.route("/approve_seller",  methods= ['POST'])
def approve_seller():
    print("yo")
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

def get_sellers():
    dbCursor = db.cursor()
    sqlQuery = 'Select * from seller_details;'
    dbCursor.execute(sqlQuery)
    res = dbCursor.fetchall() # List of tuples
    seller = []
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
    print("Done")
    return seller