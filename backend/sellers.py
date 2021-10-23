from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json

sellers = Blueprint('sellers',__name__)

seller = [
      {
        'id': 0,
        'name': "A",
        'description': "Groceries",
      },
      {
        'id': 1,
        'name': "B",
        'description': "Clothes",
      },
      {
        'id': 2,
        'name': "C",
        'description': "Electronics",
      }
  ]

@sellers.route("/sellers")
def get_sellers():
    return json.dumps(get_sellers(), separators=(',', ':'))

@sellers.route("/approve_seller",  methods= ['POST'])
def approve_seller():
  return 'approved'

def get_sellers():
    return seller