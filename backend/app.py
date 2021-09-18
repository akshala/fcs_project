from flask import Flask
import json

import products

app = Flask(__name__)

@app.route("/")
def hello():
    return {"Hello" : ['1', '2', '3']}

@app.route("/products")
def get_products():
    return json.dumps(products.get_products(), separators=(',', ':'))

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'
    return response

if __name__ == 'main':
    app.run(debug=True)