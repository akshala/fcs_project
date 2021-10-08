from flask import Flask
import json
# import products
from . import db

products = [
      {
        'id': 0,
        'name': "Laptop",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Electronics'
      },
      {
        'id': 1,
        'name': "Bedsheet",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Household'
      },
      {
        'id': 2,
        'name': "Badminton",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Sports'
      },
      {
        'id': 3,
        'name': "Laptop",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Electronics'
      },
      {
        'id': 4,
        'name': "Laptop",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Electronics'
      }
  ]

app = Flask(__name__)

@app.route("/")
def hello():
    return {"Hello" : ['1', '2', '3']}

@app.route("/products")
def get_products():
    return json.dumps(products, separators=(',', ':'))#products.get_products(), separators=(',', ':'))

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'
    return response

if __name__ == 'main':
    app.run(debug=True)