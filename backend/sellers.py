from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json
from os import urandom
import db_helper

sellers = Blueprint('sellers',__name__)

@sellers.route("/sellers")
def get_sellers():
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None
    if not user:
        return []
    if user['role'] != "Admin":
        return []
    return json.dumps(get_sellers_helper(), separators=(',', ':'))

@sellers.route("/approve_seller",  methods= ['POST'])
def approve_seller():
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None
    if not user:
        return []
    if user['role'] != "Admin":
        return []

    data = json.loads(request.data)
    username = data['username']
    
    return db_helper.approve_seller_in_db(username)

@sellers.route("/delete_seller",  methods= ['POST'])
def delete_seller():
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None
    if not user:
        return []
    if user['role'] != "Admin":
        return []
        
    data = json.loads(request.data)
    username = data['username']
    
    return db_helper.delete_seller(username)

def get_sellers_helper():
    return db_helper.get_sellers_from_db()