from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json

import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

products = Blueprint('products',__name__)

all_products = {
      0: {
        'id': 0,
        'name': "Laptop",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Electronics',
        'price': 75000,
        'seller': 'jkdn83iw93'
      },
      1: {
         'id': 1,
        'name': "Bedsheet",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Household',
        'price': 1500,
        'seller': 'jkdn83iw93'
      },
      2: {
        'id': 2,
        'name': "Badminton",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Sports',
        'price': 500,
        'seller': 'jkdn83iw93'
      },
      3: {
        'id': 3,
        'name': "Laptop",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Electronics',
        'price': 80000,
        'seller': 'jkdn83iw93'
      },
      4: {
        'id': 4,
        'name': "Laptop",
        'image': "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        'description': "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor",
        'category': 'Electronics',
        'price': 90000,
        'seller': 'jkdn83iw93'
      }
  }

@products.route("/products")
def get_products():
    return json.dumps(get_products(), separators=(',', ':'))

@products.route("/products/<string:id>")
def get_product(id):
  if request.method == 'GET':
    return json.dumps(get_product(int(id)), separators=(',', ':'))
  elif request.method == 'POST':
    print('post', id, request.form)
  elif request.method == 'DELETE':
    print('delete', id)

def get_products():
    return list(all_products.values())

def get_product(id):
  if id in all_products:
    return all_products[id]
  else:
    return None