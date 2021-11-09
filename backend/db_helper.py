import mysql.connector
import os
import hashlib
import datetime
import os
import errors

db = mysql.connector.connect(
  host="localhost",
  user=os.environ.get("USER_DB"),
  passwd=os.environ.get("PASSWORD_DB"),
  database=os.environ.get("DB")
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
    sqlQuery = 'select * from login_credentials_admin where username = %s;'
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
        dbCursor.close()
        return True
    sqlQuery = 'select * from seller_details where email = %s;'
    db.reconnect()
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if(len(res) > 0):
        dbCursor.close()
        return True
    db.reconnect()
    dbCursor = db.cursor()
    sqlQuery = 'select * from admin_details where email = %s;'
    db.reconnect()
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if(len(res) > 0):
        dbCursor.close()
        return True
    dbCursor.close()
    return False

def verify_otp(entered_otp, username):
    sqlQuery = 'select otp, time from otp_table where username = %s order by time desc;'
    val = (username, )
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    result = dbCursor.fetchall()
    dbCursor = db.close()
    if len(result) == 0:
        return errors.INVALID_USERNAME
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
    return errors.INVALID_OTP

def create_otp(username, otp):
    # delete all other tokens
    sqlQuery = 'delete from otp_table where username = %s;'
    val = (username,)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()
    sqlQuery = 'insert into otp_table values (%s, %s, %s);'
    now = datetime.datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    val = (username, otp, formatted_date)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()

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
    val = (username, password)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()

    if len(res) != 1:
        return None
    return generateToken(username)

def check_admin_login_credentials(username, password):
    sqlQuery = 'Select * from login_credentials_admin where username = %s and  password = %s;'
    val = (username, password)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if(len(res) == 0):
      dbCursor.close()
      return False

    sqlQuery = 'select email from admin_details where username = %s'
    val = (username, )
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    if(len(res) == 0):
        dbCursor.close()
        return False
    admin_email = res[0][0]
    return admin_email


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

def get_users_from_db():
    dbCursor = db.cursor()
    sqlQuery = 'Select * from user_details;'
    dbCursor.execute(sqlQuery)
    res = dbCursor.fetchall() # List of tuples
    users = []
    for elt in res:
      temp_dict = {}
      temp_dict['username'] = elt[1]
      temp_dict['name'] = elt[2]
      temp_dict['email'] = elt[3]
      temp_dict['verified'] = elt[4]
      users.append(temp_dict)
    dbCursor.close()
    return users

def delete_user(username):
    dbCursor = db.cursor()

    sqlQuery = 'delete from user_details where username = %s ;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    db.commit()

    sqlQuery = 'delete from login_credentials where username = %s ;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    db.commit()

    dbCursor.close()
    return "True"

def get_sellers_from_db():
    dbCursor = db.cursor()
    sqlQuery = 'Select * from seller_details;'
    dbCursor.execute(sqlQuery)
    res = dbCursor.fetchall() # List of tuples
    seller = []
    for elt in res:
      temp_dict = {}
      temp_dict['username'] = elt[1]
      temp_dict['name'] = elt[2]
      temp_dict['email'] = elt[3]
      temp_dict['verified'] = elt[4]
      temp_dict['approved'] = elt[5]
      seller.append(temp_dict)
    dbCursor.close()
    return seller

def delete_seller(username):
    dbCursor = db.cursor()

    sqlQuery = 'select id from products where seller_id = %s ;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    
    for elt in res:
        delete_product(elt[0], username)

    sqlQuery = 'delete from seller_details where username = %s ;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    db.commit()

    sqlQuery = 'delete from login_credentials_seller where username = %s ;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    db.commit()

    dbCursor.close()
    return "True"

def approve_seller_in_db(username):
    dbCursor = db.cursor()
    sqlQuery = 'update seller_details set approved = true where username = %s ;'
    val = (username, )
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()
    return "True"

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
            category = %s, price = %s, price_id = %s, stripe_id = %s, active = %s where id = %s and seller_id = %s;'
        val = (
            product['name'], 
            product['description'], 
            product['category'], 
            product['price'], 
            product['price_id'], 
            product['stripe_id'], 
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


def create_order(order_id, products, username):

    sqlQuery = 'insert into orders(order_id, username, date) values(%s, %s, %s);'
    val = (order_id, username, datetime.datetime.now())
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor.close()

    for i in products:
        product = get_product(i)
        product_id = i
        price = product['price']
        quantity = products[i]
        sqlQuery = 'insert into purchases(order_id, product_id, quantity, price) values(%s, %s, %s, %s);'
        val = (order_id, product_id, quantity, price)
        db.reconnect()
        dbCursor = db.cursor()
        dbCursor.execute(sqlQuery, val)
        db.commit()
        dbCursor.close()


def fulfill_order(order_id):
    sqlQuery = 'update orders set paid = true where order_id = %s;'
    val = (order_id, )
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    db.commit()
    dbCursor = db.close()


def update_profile(user, updated_name):
    if user['role'] == 'User':
        sqlQuery = 'update user_details set name = %s where username = %s;'
        val = (updated_name, user['username'])
        db.reconnect()
        dbCursor = db.cursor()
        dbCursor.execute(sqlQuery, val)
        db.commit()
        dbCursor = db.close()

    if user['role'] == 'Seller':
        sqlQuery = 'update seller_details set name = %s where username = %s;'
        val = (updated_name, user['username'])
        db.reconnect()
        dbCursor = db.cursor()
        dbCursor.execute(sqlQuery, val)
        db.commit()
        dbCursor = db.close()
    
def get_order_history(username):
    sqlQuery = 'select order_id, paid, date from orders where username = %s order by date desc;'
    val = (username,)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    order_list = res[:5]
    orders = []
    for order in order_list:
        sqlQuery = 'select product_id, name, quantity, purchases.price from purchases, products where order_id = %s and products.id = purchases.product_id;'
        val = (order[0],)
        db.reconnect()
        dbCursor = db.cursor()
        dbCursor.execute(sqlQuery, val)
        res = dbCursor.fetchall()
        dbCursor.close()
        orders.append({
            'id': order[0],
            'paid': order[1],
            'date': str(order[2]),
            'purchases': [{
                'product_id': product[0], 
                'product_name': product[1],
                'quantity': product[2],
                'price': product[3]
            } for product in res]
        })
    return orders

def get_seller_purchases(seller_id):
    sqlQuery = 'select orders.order_id, username, date, paid, product_id, name, quantity, purchases.price from orders, purchases, products where seller_id = %s and products.id = purchases.product_id and orders.order_id = purchases.order_id;'
    val = (seller_id,)
    db.reconnect()
    dbCursor = db.cursor()
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    purchases = []
    for purchase in res:
        purchases.append({
            'order_id': purchase[0],
            'username': purchase[1],
            'date': str(purchase[2]),
            'paid': purchase[3],
            'product_id': purchase[4], 
            'product_name': purchase[5],
            'quantity': purchase[6],
            'price': purchase[7]
        })
    return purchases