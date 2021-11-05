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

'''
****************************************
                Signup
****************************************
'''
def check_username_exists(username):
    
    dbCursor = db.cursor()
    sqlQuery = 'select * from login_credentials where username = %s;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if(len(res) > 0):
        dbCursor.close()
        return True
    sqlQuery = 'select * from login_credentials_seller where username = %s;'
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if(len(res) > 0):
        return True
    return False

def check_email_exists(email):

    dbCursor = db.cursor()
    sqlQuery = 'select * from user_details where email = %s;'
    val = (email, )
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    print(res)
    if(len(res) > 0):
        dbCursor.close()
        return True
    sqlQuery = 'select * from seller_details where email = %s;'
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    print(res)
    if(len(res) > 0):
        return True
    return False

def verify_otp(entered_otp, username):
    dbCursor = db.cursor()
    sqlQuery = 'select otp, time from otp_table where username = %s order by time desc;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    result = dbCursor.fetchall()
    dbCursor.close()
    otp = result[0][0]
    time = result[0][1]
    print(otp, time)
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    tdelta = datetime.strptime(formatted_date, '%Y-%m-%d %H:%M:%S') - datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    print(time, formatted_date, tdelta, tdelta.seconds)
    if otp == entered_otp and tdelta.seconds < 300:
        dbCursor = db.cursor()
        sqlQuery = 'update user_details set verified = true where username = %s ;'
        val = (username, )
        dbCursor.execute(sqlQuery, val)
        db.commit()
        sqlQuery = 'update seller_details set verified = true where username = %s ;'
        val = (username, )
        dbCursor.execute(sqlQuery, val)
        db.commit()
        dbCursor.close()
        return True
    return False

'''
****************************************
                Login
****************************************
'''
def check_login_credentials(username, password, role):
    dbCursor = db.cursor()
    if(role == 'User'):
      sqlQuery = 'Select * from user_details u, login_credentials l where u.username = %s and u.username = l.username and u.verified = true and l.password = %s;'
    elif(role == 'Seller'):
      sqlQuery = 'Select * from seller_details u, login_credentials_seller l where u.username = %s and u.username = l.username and u.verified = true and l.password = %s and u.approved = true;'
    elif role == 'Admin':
      #### DO FOR ADMIN ####
      sqlQuery = 'Select * from user_details u, login_credentials l where u.username = %s and u.username = l.username and u.verified = true and l.password = %s;'
    val = (username, password)
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()

    print(res)
    print(len(res) == 1)

    return {'status': len(res) == 1, 'access_token': generateToken(username)}

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
'''
****************************************
        User, Seller, Admin info
****************************************
'''
def get_user(username):
    pass

def get_user_from_token(token):
    # get username from token
    dbCursor = db.cursor()
    sqlQuery = 'select username, auth_token, time from auth_tokens \
        where auth_token = %s;'
    val = (token,)
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if (len(res) == 0):
        return None
    assert len(res) == 1
    user = res[0]
    if user[2] > datetime.datetime.now():
        return None
    
    return get_user(user[0])


'''
****************************************
                Products
****************************************
'''
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
    