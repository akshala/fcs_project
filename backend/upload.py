from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import os

upload = Blueprint('upload',__name__)

@upload.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join('./test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    response="File Upload Successful"
    return response