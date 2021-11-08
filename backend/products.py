from flask import Blueprint, session, request, redirect, url_for, render_template, flash, send_file
import json
from werkzeug.utils import secure_filename
import os
import payment
import db_helper
import hashlib
import input_validation_helper
import errors

products = Blueprint('products',__name__)

@products.route("/products")
def get_products():
    return json.dumps(get_products_helper(), separators=(',', ':'))


def get_products_helper():
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None
    if user and user['role'] == 'Seller':
        products = db_helper.get_products(user['username'])
    else:
        products = db_helper.get_products()
    return products 

@products.route("/products/cart", methods=['POST'])
def get_cart_products():
    return json.dumps(get_cart(request.json['cart']), separators=(',', ':'))

def get_cart(cart):
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None
    if not user or user['role'] != 'User':
        return errors.PERMISSION_DENIED
    products = []
    try:
        cart = list(cart)
    except Exception:
        return 'Incorrect Input Format'
    for product_id in cart:
        product_id = str(product_id)
        product = db_helper.get_product(product_id)
        if not product:
            return 'An error occurred'
        products.append(product)
    return products

@products.route("/products/new", methods=['POST'])
def add_product():
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None
    if not user:
        return 'Invalid Access Token'
    if user['role'] != 'Seller':
        return 'Permission Denied'
    if not user['approved']:
        return 'Please wait for admin approval for selling products'
    seller_id = user['username']

    # generate product id
    id = hashlib.sha256(os.urandom(20)).hexdigest()[:25]

    # input validation
    name = request.form['name']
    if not input_validation_helper.is_valid_string(name):
        return 'Product Name contains special characters!'

    description = request.form['description']
    if not input_validation_helper.is_valid_string(description):
        return 'Description contains special characters!'
    
    category = request.form['category']
    if not input_validation_helper.is_valid_category(category):
        return 'Category not in valid categories'
    
    price = request.form['price']
    if not input_validation_helper.is_valid_positive_int(price):
        return 'Price is not a positive integer'

    if not request.files['image_1']:
        return 'Image 1 not uploaded'
    if secure_filename(request.files['image_1'].filename)[-4].lower() not in ['.png', '.jpg']:
        return 'Invalid Image Type for image 1. Should be .jpg or .png'

    if not request.files['image_2']:
        return 'Image 2 not uploaded'
    if secure_filename(request.files['image_2'].filename)[-4].lower() not in ['.png', '.jpg']:
        return 'Invalid Image Type for image 2. Should be .jpg or .png'

    try:
        # upload image files to product_images and add the paths to database
        image_1 = request.files['image_1']
        imgPath1 = imageUpload(id, image_1)
        image_2 = request.files['image_2']
        imgPath2 = imageUpload(id, image_2)
        db_helper.add_image_for_product(id, imgPath1)
        db_helper.add_image_for_product(id, imgPath2)
    except:
        return 'Image upload failed. Please try again.'

    # create product in stripe
    res = payment.create_product(name)
    stripe_product_id = res['id']

    res = payment.create_price(stripe_product_id, price)
    stripe_price_id = res['id']

    # insert into database
    product = {
        'id': id, 
        "seller_id" : seller_id, 
        "name" : name, 
        "description" : description, 
        "category": category, 
        "price": price, 
        "price_id": stripe_price_id, 
        "stripe_id": stripe_product_id, 
        'active': True
    }
    db_helper.add_product(product)

    return 'Product created successfully'

def imageUpload(product_id, file):
    target=os.path.join('./product_images/' + product_id)
    if not os.path.isdir(target):
        os.mkdir(target)
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    return filename




@products.route("/products/<string:id>", methods=['GET', 'POST', 'DELETE'])
def product(id):
    if request.method == 'GET':
        return json.dumps(get_product(id), separators=(',', ':'))
    elif request.method == 'POST':
        return update_product(id, json.loads(request.data))
    elif request.method == 'DELETE':
        return delete_product(id)

def get_product(id):
    return db_helper.get_product(id)

def update_product(id, updates):
    # obtain seller from auth token
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    if not user:
        return 'Invalid Access Token'
    if user['role'] != 'Seller' and user['role'] != 'Admin':
        return 'Permission Denied'


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

    if user['role'] == 'Seller':
        seller_id = user['username']
        db_helper.update_product(product, seller_id)
    elif user['role'] == 'Admin':
        db_helper.update_product(product)

    return 'update success'

def delete_product(id):
    # obtain seller from auth token
    auth_header = request.headers.get('Authorization')[7:]
    user = db_helper.get_user_from_token(auth_header)
    if not user:
        return 'Invalid Access Token'
    if user['role'] == 'User':
        return 'Permission Denied'
    if user['role'] == 'Seller':
        seller_id = user['username']
        db_helper.delete_product(id, seller_id)
    else:
        db_helper.delete_product(id)
    return 'delete success'


@products.route("/product_images/<string:product_id>/<string:path>", methods=['GET'])
def product_images(product_id, path):
    return send_file('product_images/' + product_id + '/' + path)
