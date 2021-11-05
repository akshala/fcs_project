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
    username = user['username'] + '.pdf'

    filename = secure_filename(username)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    response="File Upload Successful"
    return response

@upload.route('/get_document', methods=['GET'])
def displayPdf():
    query = str(request.query_string)[2:-1]
    dataO = query.split('&')
    data = {}
    for d in dataO:
        temp = d.split('=')
        data[temp[0]] = temp[1]
    username = data['username'] + '.pdf'
    return send_file('./test_docs/' + username)