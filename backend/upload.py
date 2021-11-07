from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from flask import send_file, send_from_directory, safe_join, abort, make_response
from flask import make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import os
import db_helper

upload = Blueprint('upload',__name__)

@upload.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join('./test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 
    user = db_helper.get_user_from_token(request.headers['Authorization'][7:])
    if not user:
        return 'Invalid Auth Token'
    if user['role'] != 'Seller':
        return 'Permission Denied'
    if user['approved']:
        return 'You are an already approved seller'
    username = user['username'] + '.pdf'

    filename = secure_filename(username)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    response="File Upload Successful"
    return response

@upload.route('/get_document/<string:filename>?token=<string:token>', methods=['GET'])
def displayPdf(filename, token):
    user = db_helper.get_user_from_token(token)
    username = filename + '.pdf'
    return send_file('./test_docs/' + username)