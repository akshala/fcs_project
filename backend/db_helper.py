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
    
    sqlQuery = 'select * from login_credentials where username = %s;'
    val = (username, )
    db.reconnect()
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if(len(res) > 0):
        return True
    sqlQuery = 'select * from login_credentials_seller where username = %s;'
    db.reconnect()
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if(len(res) > 0):
        return True
    return False

def check_email_exists(email):

    sqlQuery = 'select * from user_details where email = %s;'
    val = (email, )
    db.reconnect()
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if(len(res) > 0):
            return True
    dbCursor.close()
    sqlQuery = 'select * from seller_details where email = %s;'
    db.reconnect()
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    db.reconnect()
    dbCursor = db.cursor()
    if(len(res) > 0):
        return True
    return False

def verify_otp(entered_otp, username):
    print(entered_otp, username)
    sqlQuery = 'select otp, time from otp_table where username = %s order by time desc;'
    val = (username, )
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    result = dbCursor.fetchall()
    dbCursor = db.close()
    if len(result) == 0:
        return 'Invalid Username'
    otp = result[0][0]
    time = result[0][1]
    now = datetime.datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    tdelta = datetime.datetime.strptime(formatted_date, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    if otp == entered_otp and tdelta.seconds < 300:
        sqlQuery = 'update user_details set verified = true where username = %s ;'
        val = (username, )
        db.reconnect()
        dbCursor = db.cursor()
        dbCursor.execute(sqlQuery, val)
        db.commit()
        dbCursor = db.close()
        sqlQuery = 'update seller_details set verified = true where username = %s ;'
        val = (username, )
        db.reconnect()
        dbCursor = db.cursor()
        dbCursor.execute(sqlQuery, val)
        db.commit()
        dbCursor.close()
        return 'true ' + generateToken(username)
    return 'Invalid OTP'

'''
****************************************
                Login
****************************************
'''
def check_login_credentials(username, password, role):
    if(role == 'User'):
      sqlQuery = 'Select * from user_details u, login_credentials l where u.username = %s and u.username = l.username and u.verified = true and l.password = %s;'
    elif(role == 'Seller'):
      sqlQuery = 'Select * from seller_details u, login_credentials_seller l where u.username = %s and u.username = l.username and u.verified = true and l.password = %s and u.verified = true;'
    elif role == 'Admin':
      #### DO FOR ADMIN ####
      sqlQuery = 'Select * from user_details u, login_credentials l where u.username = %s and u.username = l.username and u.verified = true and l.password = %s;'
    val = (username, password)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()

    print(res)
    print(len(res) == 1)

    if len(res) != 1:
        return None
    return generateToken(username)

def generateToken(username):
    # generate a random hash
    hash_ = hashlib.sha256(os.urandom(50)).hexdigest()
    validity = datetime.datetime.now() + datetime.timedelta(days=1)
    
    # delete all other tokens
    sqlQuery = 'delete from auth_tokens where username = %s;'
    val = (username,)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()
    # insert it into auth_token table
    sqlQuery = 'insert into auth_tokens (username, auth_token, time) \
        values ( %s, %s, %s);'
    val = (username, hash_, validity)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()

    return hash_
'''
****************************************
        User, Seller, Admin info
****************************************
'''
def get_user(username):
    sqlQuery = 'select username, name, email, verified from user_details where username = %s;'
    val = (username,)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if len(res) == 1:
        return {
            'username': res[0][0],
            'role': 'User',
            'name': res[0][1],
            'email': res[0][2],
            'verified': res[0][3]
        }
    sqlQuery = 'select username, name, email, verified, approved from seller_details where username = %s;'
    val = (username,)
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if len(res) == 1:
        return {
            'username': res[0][0],
            'role': 'Seller',
            'name': res[0][1],
            'email': res[0][2],
            'verified': res[0][3],
            'approved': res[0][4]
        }
    sqlQuery = 'select username, email from admin_details where username = %s;'
    val = (username,)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if len(res) == 1:
        return {
            'username': res[0][0],
            'role': 'Admin',
            'email': res[0][1],
        }
    return None

def get_user_from_token(token):
    # get username from token
    sqlQuery = 'select username, auth_token, time from auth_tokens \
        where auth_token = %s;'
    val = (token,)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if (len(res) == 0):
        return None
    assert len(res) == 1
    user = res[0]
    if user[2] < datetime.datetime.now():
        return None
    return get_user(user[0])


'''
****************************************
                Products
****************************************
'''
def get_products(seller_id = None):
    if not seller_id:
        sqlQuery = 'select id, seller_id, name, description, category, \
        price, price_id, stripe_id, active from products where active = TRUE;'
        db.reconnect()
        dbCursor = db.cursor()
        dbCursor.execute(sqlQuery)
    else:
        sqlQuery = 'select id, seller_id, name, description, category, \
        price, price_id, stripe_id, active from products where seller_id = %s and active = TRUE;'
        val = (seller_id,)
        db.reconnect()
        dbCursor = db.cursor()
        dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
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
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()

def get_product(prod_id):
    sqlQuery = 'select id, seller_id, name, description, category, \
        price, price_id, stripe_id, active from products where id = %s and active = TRUE;'
    val = (prod_id,)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
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

def update_product(product, seller_id = None):
    if seller_id == None:
        sqlQuery = 'update products set name = %s, description = %s, \
            category = %s, price = %s, price_id = %s, stripe_id = %s, active = %s where id = %s;'
        val = (
            product['name'], 
            product['description'], 
            product['category'], 
            product['price'], 
            product['price_id'], 
            product['stripe_id'], 
            product['active'],
            product['id']
        )
    else:
        sqlQuery = 'update products set name = %s, description = %s, \
            category = %s, price = %s, active = %s where id = %s and seller_id = %s;'
        val = (
            product['name'], 
            product['description'], 
            product['category'], 
            product['price'], 
            product['active'],
            product['id'],
            seller_id
        )
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()

def delete_product(id, seller_id = None):
    if seller_id == None:
        sqlQuery = 'update products set active = %s where id = %s;'
        val = (False, id)
    else:
        sqlQuery = 'update products set active = %s where id = %s and seller_id = %s;'
        val = (False, id, seller_id)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()
    return True


def add_image_for_product(product_id, img_path):
    sqlQuery = 'insert into images(product_id, img_path) values(%s, %s);'
    val = (product_id, img_path)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()

def get_images_for_product(product_id):
    sqlQuery = 'select img_path from images where product_id = %s;'
    val = (product_id,)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    return list(map(lambda row: row[0], res))
    