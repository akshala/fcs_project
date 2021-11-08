from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json
from os import urandom
import db_helper

users = Blueprint('users',__name__)

@users.route("/users")
def get_users():
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None
    if not user:
        return json.dumps([])
    if user['role'] != "Admin":
        return json.dumps([])
    return json.dumps(db_helper.get_users_from_db(), separators=(',', ':'))


@users.route("/delete_user",  methods= ['POST'])
def delete_users():
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None    
    if not user:
        return json.dumps([])
    if user['role'] != "Admin":
        return json.dumps([])
    
    data = json.loads(request.data)
    username = data['username']
    return db_helper.delete_user(username)
