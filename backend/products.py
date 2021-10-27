from flask import Blueprint, session, request, redirect, url_for, render_template, flash, send_file
import json
from werkzeug.utils import secure_filename
import os
import payment
import db_helper
import hashlib

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

def get_products():
    products = db_helper.get_products()
    print(products)
    return products 

@products.route("/products/new", methods=['POST'])
def add_product():
    if request.method == 'POST':
        print('post', request.data)

        # generate later
        id = hashlib.sha256(os.urandom(20)).hexdigest()[:25]

        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']

        # upload image files to product_images and add the paths to database
        imgPath1 = imageUpload(name, request.files['image_1'])
        imgPath2 = imageUpload(name, request.files['image_2'])
        db_helper.add_image_for_product(id, imgPath1)
        db_helper.add_image_for_product(id, imgPath2)

        # create product in stripe
        res = payment.create_product(name)
        stripe_product_id = res['id']

        res = payment.create_price(stripe_product_id, price)
        stripe_price_id = res['id']

        # insert into database
        product = {
          'id': '0', 
          "seller_id" : '0', 
          "name" : name, 
          "description" : description, 
          "category": category, 
          "price": price, 
          "price_id": stripe_price_id, 
          "stripe_id": stripe_product_id, 
          'active': True
        }
        db_helper.add_product(product)

        return 'create success'

def imageUpload(product_name, file):
    target=os.path.join('./product_images')
    if not os.path.isdir(target):
        os.mkdir(target)
    filename =  product_name + '_' + secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    return filename




@products.route("/products/<string:id>", methods=['GET', 'POST', 'DELETE'])
def product(id):
    if request.method == 'GET':
        return json.dumps(get_product(int(id)), separators=(',', ':'))
    elif request.method == 'POST':
        print('post', id, request.data)
        return update_product(id, json.loads(request.data))
    elif request.method == 'DELETE':
        print('delete', id)
        return delete_product(id)

def get_product(id):
    return db_helper.get_product(id)

def update_product(id, updates):

    old_product = db_helper.get_product(id)

    product = dict(old_product)

    if 'name' in updates:
        product['name'] = updates['name']
    if 'description' in updates:
        product['description'] = updates['description']
    if 'category' in updates:
        product['category'] = updates['category']
    if 'price' in updates:
        product['price'] = updates['price']

    # Reassign price in stripe if changed
    if product['price'] != old_product['price']:
        payment.update_price(product['price_id'], False)
        res = payment.create_price(product['stripe_id'], product['price'])
        stripe_price_id = res['id']
        product['price_id'] = stripe_price_id

    db_helper.update_product(product)
  
    return 'update success'

def delete_product(id):
    db_helper.delete_product(id)
    return 'delete success'


@products.route("/product_images/<string:path>", methods=['GET'])
def product_images(path):
    return send_file('product_images/' + path)
