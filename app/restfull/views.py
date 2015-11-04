from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from app import app
from app import mongoCategoryDetails, categoryListingFilter, mongoProductmaster
from app.decorators import jsonResponse
from app.products.products import *

mod = Blueprint('restful', __name__, url_prefix='/restfull')

@mod.route('/hello2', methods=['GET'])
def hello2():
	return "hello2"

@mod.route('/categories', methods=['GET'])
@jsonResponse
def getCategories():
	Categories = mongoCategoryDetails.find()
	Categories = [cat['type'] for cat in Categories]
	allCategories = {}
	allCategories['categories'] = Categories
	return Categories

@mod.route('/brands/<category>', methods=['GET'])
@jsonResponse
def getAllBrands(category):
	
	category_products = mongoProductmaster.find({'category':category})
	brand_list = [prod['brand'] for prod in category_products]
	brand_list = list(set(brand_list))
	return brand_list

@mod.route('/products/<category>/<brand>', methods=['GET'])
@jsonResponse
def getAllProducts(category, brand):
	product_list = []
	brand_products = mongoProductmaster.find({'category':category, 'brand':brand})
	prodList = {}
	for prod in brand_products:
		prodList[prod['product_name']] = prod['product_id']
	
	return prodList

@mod.route('/productnames/<category>/<brand>', methods=['GET'])
@jsonResponse
def getAllProduct_name(category, brand):
	product_list = []
	brand_products = mongoProductmaster.find({'category':category, 'brand':brand})
	product_list = [prod['product_name'] for prod in brand_products]
	return product_list

@mod.route('/price/<product_id>', methods=['GET'])
@jsonResponse
def getProductDetail(product_id):	
	return getProductPrice(product_id)

@mod.route('/categorydetails', methods=['GET'])
@jsonResponse
def getAllCategoryDetails():
	Categories = mongoCategoryDetails.find()
	allCategoriesDict = {}
	for doc in Categories:
		allCategoriesDict[doc['type']] = doc
	return allCategoriesDict


