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

product = [
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

@products.route("/products")
def get_products():
    return json.dumps(get_products(), separators=(',', ':'))

def get_products():
    return product