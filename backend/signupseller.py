from flask import Blueprint, session, request, redirect, url_for, render_template, flash
import json
from os import urandom


import mysql.connector
db = mysql.connector.connect(
  host="localhost",
  user="root_admin",
  passwd="FCS@aopv@1234",
  database="amawon"
)

signupseller = Blueprint('signupseller',__name__)
