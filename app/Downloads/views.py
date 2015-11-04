from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, make_response
from app.util import getArgAsList
from app.products.products import *
from app import mongoProductmaster, mongoProductSpecification, mongoProductPrice, mongoKeywords, mongoReviews
mod = Blueprint('downloads', __name__, url_prefix='/downloads')

@mod.route('/allproducts', methods=['GET'])
def getAllProducts():
	try:
		category = getArgAsList(request, 'category')[0]
	except:
		category = None
	if category:
		allProducts  = mongoProductmaster.find({"category":category})
	else:
		allProducts  = mongoProductmaster.find()

	csvStrings= []
	csvList = []
	for product in allProducts:
		product_id = product['product_id']
		priceDict, min_priceDict = getProductPrice(product_id)
		category = product['category']
		brand = product['brand']
		
		try:
			lowestprice = str(min_priceDict['price'])
		except:
			lowestprice = ""
		keywordsRating = getProductRating(product_id)
		rating = 0.0
		sumC = 0
		for keyword in keywordsRating:
			rating = rating + float(keyword['rating'])
			sumC = sumC + 1
		if sumC != 0:
			rating = rating/sumC
		rating = str(rating)
		rowList = [product_id, brand, lowestprice, category, rating]
		csvList.append(rowList)
	 
	for csvLine in csvList:
		csvStrings += [",".join(csvLine)]
	csvStrings =  "\n".join(csvStrings)
	response = make_response(csvStrings)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
	response.headers["Content-Disposition"] = "attachment; filename=" + category + "_allProducts.csv"
	return response 
