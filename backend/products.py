from flask import Blueprint, session, request, redirect, url_for, render_template, flash, send_file
import json
from werkzeug.utils import secure_filename
import os
import payment
import db_helper
import hashlib
import input_validation_helper
import errors
import requests

products = Blueprint('products',__name__)

CAPTCHA_SECRET_KEY = os.environ.get("CAPTCHA_SECRET_KEY")

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
    print(cart)
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
        return errors.INCORRECT_INPUT_FORMAT
    for product_id in cart:
        product_id = str(product_id)
        product = db_helper.get_product(product_id)
        if not product:
            return errors.ERROR_OCCURED
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
        return errors.INVALID_ACCESS_TOKEN
    if user['role'] != 'Seller':
        return errors.PERMISSION_DENIED
    if not user['approved']:
        return errors.WAIT_ADMIN_APPROVAL
    seller_id = user['username']

    # generate product id
    id = hashlib.sha256(os.urandom(20)).hexdigest()[:25]

    captcha_data = { "secret": CAPTCHA_SECRET_KEY, "response": request.form['captcha']}

    x = requests.post("https://www.google.com/recaptcha/api/siteverify", data = captcha_data)

    if x.json()['success'] != True:
        return errors.CAPTCHA_FAILED

    # input validation
    name = request.form['name']
    if not input_validation_helper.is_valid_string(name):
        return errors.PRODUCT_NAME_INPUT_VALIDATION

    description = request.form['description']
    if not input_validation_helper.is_valid_string(description):
        return errors.PRODUCT_DESCRIPTION_INPUT_VALIDATION
    
    category = request.form['category']
    if not input_validation_helper.is_valid_category(category):
        return errors.PRODUCT_CATEGORY_INPUT_VALIDATION
    
    price = request.form['price']
    if not input_validation_helper.is_valid_positive_int(price):
        return errors.PRICE_INPUT_VALIDATION

    if len(request.files) < 2:
        return errors.IMAGES_COUNT_VALIDATION
    for file in request.files:
        if secure_filename(request[file].filename)[-4:].lower() not in ['.png', '.jpg']:
            return errors.IMAGES_TYPE_VALIDATION

    # upload image files to product_images and add the paths to database
    count = 1
    for file in request.files:
        try:
            image = request.files[file]
            imgPath = imageUpload(id, image, str(count))
            db_helper.add_image_for_product(id, imgPath)
            count += 1
        except:
            return errors.IMAGE_UPLOAD_FAILED

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

    return errors.SUCCESS


def imageUpload(product_id, file, filname):
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
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None
    if not user:
        return errors.INVALID_AUTH_TOKEN
    if user['role'] != 'Seller' and user['role'] != 'Admin':
        return errors.PERMISSION_DENIED

    captcha_data = { "secret": CAPTCHA_SECRET_KEY, "response": updates['captcha']}

    x = requests.post("https://www.google.com/recaptcha/api/siteverify", data = captcha_data)

    if x.json()['success'] != True:
        return errors.CAPTCHA_FAILED

    old_product = db_helper.get_product(id)

    product = dict(old_product)

    if 'name' in updates:
        if not input_validation_helper.is_valid_string(updates['name']):
            return errors.PRODUCT_NAME_INPUT_VALIDATION
        product['name'] = updates['name']
    if 'description' in updates:
        if not input_validation_helper.is_valid_string(updates['description']):
            return errors.PRODUCT_DESCRIPTION_INPUT_VALIDATION
        product['description'] = updates['description']
    if 'category' in updates:
        if not input_validation_helper.is_valid_category(updates['category']):
            return errors.PRODUCT_CATEGORY_INPUT_VALIDATION
        product['category'] = updates['category']
    if 'price' in updates:
        if not input_validation_helper.is_valid_positive_int(updates['price']):
            return errors.PRICE_INPUT_VALIDATION
        product['price'] = updates['price']

    # Reassign price in stripe if changed
    if product['price'] != old_product['price']:
        payment.update_price(product['price_id'], False)
        res = payment.create_price(product['stripe_id'], product['price'])
        if not res:
            return errors.ERROR_OCCURED
        stripe_price_id = res['id']
        product['price_id'] = stripe_price_id

    if user['role'] == 'Seller':
        seller_id = user['username']
        db_helper.update_product(product, seller_id)
    elif user['role'] == 'Admin':
        db_helper.update_product(product)

    return errors.SUCCESS

def delete_product(id):
    if request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')[7:]
        user = db_helper.get_user_from_token(auth_header)
    else:
        user = None
    if not user:
        return errors.INVALID_ACCESS_TOKEN
    if user['role'] == 'Seller':
        seller_id = user['username']
        db_helper.delete_product(id, seller_id)
    elif user['role'] == 'Admin':
        db_helper.delete_product(id)
    else:
        return errors.PERMISSION_DENIED
    return errors.SUCCESS


@products.route("/product_images/<string:product_id>/<string:filename>", methods=['GET'])
def product_images(product_id, filename):
    return send_file('product_images/' + product_id + '/' + filename)
