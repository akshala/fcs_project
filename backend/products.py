from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json
from werkzeug.utils import secure_filename
import os
# from payment import *

import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

products = Blueprint('products',__name__)

all_products = {
      0: {
        'id': 0,
        'name': "Laptop",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Electronics',
        'price': 75000,
        'seller': 'jkdn83iw93'
      },
      1: {
         'id': 1,
        'name': "Bedsheet",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Household',
        'price': 1500,
        'seller': 'jkdn83iw93'
      },
      2: {
        'id': 2,
        'name': "Badminton",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Sports',
        'price': 500,
        'seller': 'jkdn83iw93'
      },
      3: {
        'id': 3,
        'name': "Laptop",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Electronics',
        'price': 80000,
        'seller': 'jkdn83iw93'
      },
      4: {
        'id': 4,
        'name': "Laptop",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Electronics',
        'price': 90000,
        'seller': 'jkdn83iw93'
      }
  }

@products.route("/products")
def get_products():
  # if request.headers.get('Authorization')
    return json.dumps(get_products(), separators=(',', ':'))

@products.route("/products/new", methods=['POST'])
def add_product():
  if request.method == 'POST':
    print('post', request.data)
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    fileUpload(request.files['image_1'])
    fileUpload(request.files['image_2'])
    return 'create success'

def fileUpload(product_name, file):
    target=os.path.join('./product_images')
    if not os.path.isdir(target):
        os.mkdir(target)
    filename =  product_name + '_' + secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    response="File Upload Successful"
    return response


@products.route("/products/<string:id>", methods=['GET', 'POST', 'DELETE'])
def get_product(id):
  if request.method == 'GET':
    return json.dumps(get_product(int(id)), separators=(',', ':'))
  elif request.method == 'POST':
    print('post', id, request.data)
    return 'update success'
  elif request.method == 'DELETE':
    print('delete', id)
    return 'delete success'


def get_products():
    return list(all_products.values())

def get_product(id):
  if id in all_products:
    return all_products[id]
  else:
    return None