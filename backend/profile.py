from flask import Blueprint, session, request
import db_helper
import errors
import json
import input_validation_helper

profile = Blueprint('profile',__name__)

@profile.route("/profile", methods = ['GET', 'POST'])
def profile_():
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None
    if not user:
        return {'error': errors.INVALID_AUTH_TOKEN}
    if request.method == 'GET':
        return json.dumps(get_profile(), separators=(',', ':'))
    if request.method == 'POST':
        db_helper.update_profile(user, request.data)
        return errors.SUCCESS
    return errors.ERROR_OCCURED

def get_profile():
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None
    if not user:
        return {'error': errors.INVALID_AUTH_TOKEN}
    if user['role'] == 'User':
        user['orders'] = db_helper.get_order_history(user['username'])
    elif user['role'] == 'Seller':
        user['purchases'] = db_helper.get_seller_purchases(user['username'])
    return user