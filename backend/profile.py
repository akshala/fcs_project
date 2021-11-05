from flask import Blueprint, session, request
import db_helper
import errors
import json

profile = Blueprint('profile',__name__)

@profile.route("/profile")
def get_profile():
    return json.dumps(get_profile(), separators=(',', ':'))

def get_profile():
    auth_header = request.headers.get('Authorization')[7:]
    print(auth_header)
    user = db_helper.get_user_from_token(auth_header)
    print(user)
    if user:
        return user
    else:
        return {'error': errors.INVALID_AUTH_TOKEN}
