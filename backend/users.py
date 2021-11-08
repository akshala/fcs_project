from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json
from os import urandom
import db_helper

users = Blueprint('users',__name__)

@users.route("/users")
def get_users():
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    if not user:
        return []
    if user['role'] != "Admin":
        return []
    return json.dumps(db_helper.get_users_from_db(), separators=(',', ':'))


@users.route("/delete_user",  methods= ['POST'])
def delete_users():
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    
    if not user:
        return []
    if user['role'] != "Admin":
        return []
    
    data = json.loads(request.data)
    username = data['username']
    return db_helper.delete_user(username)
