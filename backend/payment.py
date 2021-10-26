import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.environ.get("STRIPE_API_KEY")

def create_product(name):
	try:
		res = stripe.Product.create(name = name)
		return res
	except Exception as e:
		print (e)
		print ("[-] ERROR: An error occured while creating a product.")


def update_product(product_id, active = True):
	try:
		res = stripe.Product.modify(product_id, active = active)
		return res
	except Exception as e:
		print (e)
		print ("[-] ERROR: An error occured while updating the product")

def get_product_list():
	try:
		res = stripe.Product.list()
		return res
	except Exception as e:
		print (e)
		print ("[-] ERROR: Unable to fetch product list")

def remove_product(product_id):
	try:
		res = stripe.Product.delete(product_id)
	except Exception as e:
		print (e)
		print ("[-] ERROR: An error occured while removing object with id " + product_id)
		return None
	if res['deleted'] == True:
		return "Product removed successfully"
	else:
		return "Failed to remove product due to unknown error"

def retrieve_product_info(product_id):
	try:
		res = stripe.Product.retrieve(product_id)
		return res
	except Exception as e:
		print (e)
		print ("[-] ERROR: An error occured while retrieving the information of the product with id " + product_id)

def create_price(product_id, price):
	try:
		res = stripe.Price.create(
			unit_amount = int(price)*100,
			currency = 'inr',
			product = product_id
			)
		return res
	except Exception as e:
		print (e)
		print ("[-] ERROR: An error occured while creating the price object")

def retrieve_price(price_id):
	try:
		res = stripe.Price.retrieve(price_id)
		return res
	except Exception as e:
		print (e)
		print ("[-] ERROR: An error occured while retrieving the price object with id " + price_id)

def update_price(price_id, active = True):
	try:
		res = stripe.Price.modify(price_id, active = active)
		return res
	except Exception as e:
		print (e)
		print ("[-] ERROR: An error occured while updating the price object with id " + price_id)
	
def get_all_price_objects():
	try:
		res = stripe.Price.list()
		return res
	except Exception as e:
		print (e)
		print ("[-] ERROR: Unable to fetch product list")