from flask import Flask
import random
import gmpy2
import json
import traceback
 
app = Flask(__name__)

@app.errorhandler(Exception)
def unhandled_exception(e):
    response = dict()
    error_message = traceback.format_exc()
    app.logger.error("Caught Exception: {}".format(error_message))
    response["errorMessage"] = error_message
    return response, 500

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = 'https://localhost:3000'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'
    return response

def encrypt(m, d, n):
    c = pow(m, d, n)
    return c

def getPublicKey():
    public_key = open('./ca_key.pub', 'r', encoding='utf-8-sig').read()
    return public_key

def getPrivateKey():
    private_key = open('./ca_key.pem', 'r', encoding='utf-8-sig').read()
    return private_key

@app.route('/generate_certificate')
def generate_certificate():
    m = random.randint(10**1022, 10**1023-1)
    private_key = gmpy2.mpz(getPrivateKey())
    public_key = gmpy2.mpz(getPublicKey())
    return json.dumps({'m': str(m), 'public_key_CA': getPublicKey(), 'enc_m': str(encrypt(m, private_key, public_key))})

@app.route('/get_public_key')
def get_public_key():
    return json.dumps({'public_key_CA': getPublicKey()})

if __name__ == '__main__':
    app.run(port='7000')