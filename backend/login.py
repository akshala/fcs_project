from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json
from os import urandom
import db_helper
import input_validation_helper

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
    if not input_validation_helper.is_valid_string(username):
      'Username contains special characters'

    password = data['password']

    role = data['role']
    if not input_validation_helper.is_valid_role(role):
      'Role not valid'

    login = db_helper.check_login_credentials(username, password, role)
    if login['status']:
    	return 'true ' + login['access_token']
    else:
      return "Username or Password is incorrect"
