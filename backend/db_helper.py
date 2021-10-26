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

def checkToken(username, token):
    # verify if token is valid
    dbCursor = db.cursor()
    sqlQuery = 'select username, auth_token, time from auth_tokens \
        where username = %s and auth_token = %s;'
    val = (username, token)
    dbCursor.execute(sqlQuery, val)
    res = dbCursor.fetchall()
    print(res)
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


generateToken('temp')
generateToken('temp')