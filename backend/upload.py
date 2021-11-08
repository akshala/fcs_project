from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from flask import send_file, send_from_directory, safe_join, abort, make_response
from flask import make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import os
import db_helper
import errors

upload = Blueprint('upload',__name__)

@upload.route('/upload', methods=['POST'])
def fileUpload():
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None

    target=os.path.join('./test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 
    if not user:
        return errors.INVALID_AUTH_TOKEN
    if user['role'] != 'Seller':
        return errors.PERMISSION_DENIED
    if user['approved']:
        return errors.ALREADY_APPROVED
    username = user['username'] + '.pdf'

    filename = secure_filename(username)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    return errors.SUCCESS

@upload.route('/get_document/<string:filename>/<string:token>', methods=['GET'])
def displayPdf(filename, token):
    user = db_helper.get_user_from_token(token)
    if user['role'] != 'Admin':
        return errors.PERMISSION_DENIED
    username = filename + '.pdf'
    return send_file('./test_docs/' + username)