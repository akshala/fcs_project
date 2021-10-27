import mysql.connector
import os
import hashlib
import datetime

db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

def checkToken(username, token):
    # verify if token is valid
    dbCursor = db.cursor()
    sqlQuery = 'select username, auth_token, time from auth_tokens \
        where username = %s and auth_token = %s;'
    val = (username, token)
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if (len(res) == 0):
        return False
    return res[0][-1] > datetime.datetime.now()

def generateToken(username):
    # generate a random hash
    hash_ = hashlib.sha256(os.urandom(50)).hexdigest()
    validity = datetime.datetime.now() + datetime.timedelta(days=1)
    
    # delete all other tokens
    dbCursor = db.cursor()
    sqlQuery = 'delete from auth_tokens where username = %s;'
    val = (username,)
    dbCursor.execute(sqlQuery, val)
    db.commit()

    # insert it into auth_token table
    dbCursor = db.cursor()
    sqlQuery = 'insert into auth_tokens (username, auth_token, time) \
        values ( %s, %s, %s);'
    val = (username, hash_, validity)
    dbCursor.execute(sqlQuery, val)
    db.commit()

    return hash_


def get_products(seller_id = None):
    dbCursor = db.cursor()
    if not seller_id:
        sqlQuery = 'select id, seller_id, name, description, category, \
        price, price_id, stripe_id, active from products where active = TRUE;'
        dbCursor.execute(sqlQuery)
    else:
        sqlQuery = 'select id, seller_id, name, description, category, \
        price, price_id, stripe_id, active from products where seller_id = %s and active = TRUE;'
        val = (seller_id, True)
        dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    products = []
    for record in res:
        product = {
            'id': record[0], 
            'seller_id' : record[1], 
            'name' : record[2], 
            'description' : record[3], 
            'category': record[4], 
            'price': record[5], 
            'price_id': record[6], 
            'stripe_id': record[7], 
            'active': record[8],
            'images': get_images_for_product(record[0])
        }
        products.append(product)
    return products


def add_product(product):
    dbCursor = db.cursor()
    sqlQuery = 'insert into products (id, seller_id, name, description, category, price, price_id, stripe_id, active) \
        values ( %s, %s, %s, %s, %s, %s, %s, %s, %s);'
    val = (
        product['id'], 
        product['seller_id'], 
        product['name'], 
        product['description'], 
        product['category'], 
        product['price'], 
        product['price_id'], 
        product['stripe_id'], 
        product['active']
    )
    dbCursor.execute(sqlQuery, val)
    db.commit()

def get_product(prod_id):
    dbCursor = db.cursor()
    sqlQuery = 'select id, seller_id, name, description, category, \
        price, price_id, stripe_id, active from products where id = %s and active = TRUE;'
    val = (prod_id,)
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if len(res) == 0:
        return None
    res = res[0]
    product = {
        'id': res[0], 
        'seller_id' : res[1], 
        'name' : res[2], 
        'description' : res[3], 
        'category': res[4], 
        'price': res[5], 
        'price_id': res[6], 
        'stripe_id': res[7], 
        'active': res[8],
        'images': get_images_for_product(res[0])
    }

    return product

def update_product(product):
    dbCursor = db.cursor()
    sqlQuery = 'update products set seller_id = %s, name = %s, description = %s, \
        category = %s, price = %s, price_id = %s, stripe_id = %s, active = %s where id = %s;'
    val = (
        product['seller_id'], 
        product['name'], 
        product['description'], 
        product['category'], 
        product['price'], 
        product['price_id'], 
        product['stripe_id'], 
        product['active'],
        product['id']
    )
    dbCursor.execute(sqlQuery, val)
    db.commit()

def delete_product(id):
    dbCursor = db.cursor()
    sqlQuery = 'update products set active = %s where id = %s;'
    val = (False, id)
    dbCursor.execute(sqlQuery, val)
    db.commit()


def add_image_for_product(product_id, img_path):
    dbCursor = db.cursor()
    sqlQuery = 'insert into images(product_id, img_path) values(%s, %s);'
    val = (product_id, img_path)
    dbCursor.execute(sqlQuery, val)
    db.commit()

def get_images_for_product(product_id):
    dbCursor = db.cursor()
    sqlQuery = 'select img_path from images where product_id = %s;'
    val = (product_id,)
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    return list(map(lambda row: row[0], res))
    