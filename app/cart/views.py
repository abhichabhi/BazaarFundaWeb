from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from bson.objectid import ObjectId

from bson import json_util
import json
import logging
from logging.handlers import RotatingFileHandler
from app import app
from app.products.products import *

from app.decorators import mongoJsonify, jsonResponse
from app.util import getArgAsList

mod = Blueprint('cart', __name__, url_prefix='/cart')


CART = "CART"
 
@mod.before_request
def before_request():
  if CART not in session:
  	session[CART] = {}

@mod.route('/add/<productId>', methods=['GET'])
@jsonResponse
def addToCart(productId):
	product_category = getProductMasterInfo(productId)['category']
	cartDetails = getCartDetails()
	try:
		category = getProductMasterInfo(cartDetails[0])['category']
		if category != product_category:
			session[CART] = {}
	except:
		pass

	if len(session[CART]) == 4:
		return {"status" : 512, "productId" : session[CART]}


	if productId not in session[CART]:
		session[CART][productId] = True
		# statusCode : 256   already present
		# status code  :512  4 phone already present
		app.logger.info(len(session[CART]))
		return {"status" : 200, "count": len(session[CART]), "productId" : session[CART].keys()}

	return {"status" : 256, "productId" : session[CART].keys() }

@mod.route('/remove/<productId>', methods=['GET'])
@jsonResponse
def removeFromCart(productId):
	
	if productId not in session[CART]:
		return {"status" : "Not in Cart!", "productId" : session[CART].keys()}

	session[CART].pop(productId, None)
	return {"status" : 200, "productId" : session[CART].keys()}

@mod.route('/get', methods=['GET'])
@jsonResponse
def getCart():
	return session[CART].keys()

def getCartDetails():
	before_request()
	cartDetails =  session[CART].keys()
	
	# app.logger.info(cartDetails)
	return cartDetails
	# cartContent = [keys for keys in cartDetails]
	
	# app.logger.info(cartContent)
	# return cartContent

@mod.route('/clear', methods=['GET'])
@jsonResponse
def clearCart():
	session[CART] = {}
	return {"status" : "true"}
