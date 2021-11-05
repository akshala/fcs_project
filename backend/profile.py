from flask import Blueprint, session, request
import db_helper
import errors
import json

profile = Blueprint('profile',__name__)

@profile.route("/profile", methods = ['GET', 'POST'])
def profile_():
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    if not user:
        return {'error': errors.INVALID_AUTH_TOKEN}
    if request.method == 'GET':
        return json.dumps(get_profile(), separators=(',', ':'))
    if request.method == 'POST':
        db_helper.update_profile(user, request.data)
        print(request)
        return 'Update Successful'
    return "Error"

def get_profile():
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    if user:
        return user
    else:
        return {'error': errors.INVALID_AUTH_TOKEN}
