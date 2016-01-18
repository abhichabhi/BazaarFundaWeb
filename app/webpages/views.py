from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from app import app
from app import mongoCategoryDetails, categoryListingFilter, mongoUserVariables
from app.products.products import *
from app.cart.views import *
from app.util import getArgAsList
from app.AdminPanel.views import getListingPageCategoryDict, getHomePageDict
from app.decorators import jsonResponse
from urlparse import urlparse, parse_qs
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
import os, thread
import json
import uuid
from app import mongoCategoryDetails
from flask.ext.social import Social
import datetime

mod = Blueprint('webpage', __name__, url_prefix='')

app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': '1435721096655907',
    'consumer_secret': '1f8fb8b82f3e84030274a6e9a368b91b'
}

@app.template_filter('space_to_underscore')
def space_to_underscore(str):
    return str.replace(" ", "_")

@app.template_filter('underscore_to_space')
def underscore_to_space(str):
    return str.replace(" ", "_")


@mod.route('/profile')
def profile():
    return render_template(
        'profile.html',
        content='Profile Page',
        twitter_conn=social.twitter.get_connection(),
        facebook_conn=social.facebook.get_connection(),
        foursquare_conn=social.foursquare.get_connection())

@mod.route('/hello2', methods=['GET'])
def hello2():
	return "hello2"
def split_space(string):
    return '_'.join(string.strip().split())

@mod.before_request
def before_request():
	app.jinja_env.filters['sjoin'] = split_space
	g.cartDetails = [getProductDetail(product_id) for product_id in getCartDetails()]
	allCategoryCursor = mongoCategoryDetails.find()
	allCategoriesDict = {}
	for doc in allCategoryCursor:
		allCategoriesDict[doc['type']] = doc	
	g.all_cat_details = allCategoriesDict
	g.recoCategory = request.args.get('recoCategory')

	allCategories = mongoCategoryDetails.find()
	allCat = []
	for cat in allCategories:
		try:
			if not cat['parent']:
				allCat.append(cat['type'])
		except:
			allCat.append(cat['type'])
	g.allCategories = allCat


@mod.route('/',methods=['GET'], strict_slashes=False)
def home():	
	title = "Bazaarfunda: Discover Products that suits your needs. Compare products and prices"
	
	# allCategories = [cat['type'] for cat in allCategories]
	allRecentProducts = getHomePageDict()['NewProducts']
	allRecentProducts = [getProductDetail(product_id) for product_id in allRecentProducts]
	allMediaPublication = getHomePageDict()['MediaPublication']
	category = "all"
	return render_template("landingpage.html", allCategories=g.allCategories, allRecentProducts=allRecentProducts,
		category=category,cartDetails=g.cartDetails, all_cat_details = g.all_cat_details,
		allMediaPublication=allMediaPublication,title=title,recoCategory=g.recoCategory)

@mod.route('/compare',methods=['GET'], strict_slashes=False)
def compare():
	cartDetails=g.cartDetails
	category = None
	categoryDetails = None
	app.logger.info('comparing')
	app.logger.info([cart['master']['product_id'] for cart in cartDetails])
	for items in cartDetails:
		if items['master']:
			category = items['master']['category']
			break
	if category:
		categoryDetails = mongoCategoryDetails.find_one({'type':category})
	if  len(cartDetails) != 0:
		title = "Bazaarfunda: Compare "
		for items in cartDetails:
			title = title + items['master']['product_name'] + " "
	else:
		title = "Bazaarfunda: Add Products to compare"
	return render_template("compare.html", cartDetails=g.cartDetails,
	 categoryDetails=categoryDetails, category=category,
	  all_cat_details = g.all_cat_details, title = title,
	   recoCategory=g.recoCategory, allCategories=g.allCategories)


@mod.route('/pdp/<product_id>/<slug>', methods=['GET'], strict_slashes=False)
@mod.route('/pdp/<product_id>', defaults={'slug': None}, methods=['GET'], strict_slashes=False)
def productDetail(product_id, slug=None):
	app.logger.info("Product Detail Page: " + product_id)
	productMasterDetails = getProductMasterInfo(product_id)
	if not slug:
		slug = productMasterDetails['surl']
		return redirect('/pdp/' + product_id + '/'+slug)
	if slug != productMasterDetails['surl']:
		slug = productMasterDetails['surl']
		return redirect('/pdp/' + product_id + '/'+slug)
	category = productMasterDetails['category']
	categoryDetails = mongoCategoryDetails.find_one({'type':category}) 
	allKeyWordsIcon = categoryDetails['allKeyWordsIcon']
	pdp_fileds = categoryDetails['pdp_fileds']
	productDetails =  getProductDetail(product_id)
	title = "Bazaarfunda: Check the user experience of " + productMasterDetails['product_name'][:30] + ".. and compare Prices"
	return render_template("product_detail.html", productMasterDetails = productMasterDetails, 
		productDetails=productDetails, allKeyWordsIcon=allKeyWordsIcon, pdp_fileds=pdp_fileds, cartDetails=g.cartDetails,
		category=category, all_cat_details = g.all_cat_details, title = title,
		allCategories=g.allCategories, recoCategory=g.recoCategory)

@mod.route('/browse/<category>/', methods=['GET'], strict_slashes=False)
def browse(category):
	app.logger.info("Listing Page: " + category)
	category_product_list = category
	filterFlag = 0	
	categoryFilterCheckedStatus = getCategoryFilterCheckedStatus()
	app.logger.info(categoryFilterCheckedStatus)
	listingStatic = getListingStatic(category)
	urlDict = urlToDict()
	millis = lambda: int(round(time.time() * 1000))
	reco_bool = 0
	print request.args
	try:
		start = int(request.args.get('start'))
	except:
		start = None 
		scoreSortedProductList = []

	if not start:
		start = 0
	# if not start:		
	# 	session['product_list'] = None
		
	# 	start = 0	
	# 	specProductIdList = getFilteredProductSpecification(request.args, category)
	# 	try:
	# 		priceRange = categoryFilterCheckedStatus['price']
	# 	except:
	# 		priceRange = None
	# 	keywords = []
	# 	weights = []
	# 	if 'keywords' in urlDict:
	# 		keywords = urlDict['keywords']
	# 	if 'weights' in urlDict:			
	# 		weights = urlDict['weights']
	# 	if 'reco' in urlDict:
	# 		reco_bool = 1
	# 	priceProductIdList = getFilteredProductPriceRange(priceRange, category)		
	# 	finalProductList = list(set(priceProductIdList) & set(specProductIdList))		
	# 	scoreSortedProductList = getScoreSortedProductID(finalProductList,category, keywords, weights)
	# 	session['product_list'] = scoreSortedProductList
	# 	utc_timestamp = datetime.datetime.utcnow()
		
	# 	try:
	# 		_sid = session['_sid']
	# 		app.logger.info("_Sid is " + str(_sid))
	# 	except:
	# 		app.logger.info( "_sid is None")
	# 		_sid = None

	# 	if _sid is not None:
	# 		try:
	# 			userDbProducts = mongoUserVariables['listing_products'].find_one({"_sid":_sid})["product_list"]
	# 			mongoUserVariables['listing_products'].update_one({"_sid":_sid}, { "$set":{ "product_list":scoreSortedProductList, "date": utc_timestamp}})
	# 		except:
	# 			mongoUserVariables['listing_products'].insert({"_sid":_sid, "product_list":scoreSortedProductList, "date": utc_timestamp})
	
	# 	else:
	# 		uid = uuid.uuid4()
	# 		_sid = uid.hex
			
	# 		mongoUserVariables['listing_products'].insert({"_sid":_sid, "product_list":scoreSortedProductList, "date": utc_timestamp})
	# 	session['_sid'] = _sid
	# 	userDbProducts = mongoUserVariables['listing_products'].find_one({"_sid":_sid})["product_list"]
	# 	scoreSortedProductList =  userDbProducts[:20]
	# else:
	# 	_sid = session['_sid']
	# 	userDbProducts = mongoUserVariables['listing_products'].find_one({"_sid":_sid})["product_list"]
	# 	scoreSortedProductList = userDbProducts[0:start+20]
	# productList = []
	# for prod in scoreSortedProductList:
	# 	prodDetail = {}
	# 	prodDetail = getProductDetail(prod['product_id'])		
	# 	productList.append(prodDetail)
	
	# totalProducts = len(userDbProducts)
	if len(categoryFilterCheckedStatus) == 0:
		filterFlag = 1

	try:
		categoryFilter = categoryListingFilter[category]
	except:
		categoryFilter = {}

	title = "Bazaarfunda: "
	if 'keywords' in urlDict:
		title = title + "Best Recommended " + category + " acording to your needs"
	else:
		title = title + "Get the best " + category + " according to other customers"
	return render_template("listing_small_prev.html", categoryFilter=categoryFilter,
	 categoryFilterCheckedStatus=categoryFilterCheckedStatus, listingStatic=listingStatic,
	 filterFlag=filterFlag, category=category, cartDetails=g.cartDetails, start=start,
	  all_cat_details = g.all_cat_details, reco_bool=reco_bool, recoCategory=g.recoCategory, title = title, allCategories=g.allCategories)


@mod.route('/listing/<category>/', methods=['GET'], strict_slashes=False)
@jsonResponse
def listing(category):
	# http://code.runnable.com/UrPpZCypQUV_AAAP/how-to-store-sessions-in-a-database-in-flask-for-python
	responseDict = {}
	category_product_list = category
	filterFlag = 0	
	categoryFilterCheckedStatus = getCategoryFilterCheckedStatus()
	urlDict = urlToDict()
	millis = lambda: int(round(time.time() * 1000))
	try:
		start = int(request.args.get('start'))
	except:
		start = None 
		scoreSortedProductList = []

	if not start or start == 0:
		session['category'] = category
		start = 0	
		specProductIdList = getFilteredProductSpecification(request.args, category)
		try:
			priceRange = categoryFilterCheckedStatus['price']
		except:
			priceRange = None
		keywords = []
		weights = []
		if 'keywords' in urlDict:
			keywords = urlDict['keywords']
		if 'weights' in urlDict:			
			weights = urlDict['weights']
		priceProductIdList = getFilteredProductPriceRange(priceRange, category)		
		finalProductList = list(set(priceProductIdList) & set(specProductIdList))		
		scoreSortedProductList = getScoreSortedProductID(finalProductList,category, keywords, weights)
		utc_timestamp = datetime.datetime.utcnow()
		
		try:
			_sid = session['_sid']
			app.logger.info("_Sid is " + str(_sid))
		except:
			app.logger.info( "_sid is None")
			_sid = None

		if _sid is not None:
			try:
				userDbProducts = mongoUserVariables['listing_products'].find_one({"_sid":_sid})["product_list"]
				mongoUserVariables['listing_products'].update_one({"_sid":_sid}, { "$set":{ "product_list":scoreSortedProductList, "date": utc_timestamp}})
			except:
				mongoUserVariables['listing_products'].insert({"_sid":_sid, "product_list":scoreSortedProductList, "date": utc_timestamp})
	
		else:
			uid = uuid.uuid4()
			_sid = uid.hex		
			mongoUserVariables['listing_products'].insert({"_sid":_sid, "product_list":scoreSortedProductList, "date": utc_timestamp})
			session['_sid'] = _sid
		print "Sid is =>", _sid, session['_sid']
		userDbProducts = mongoUserVariables['listing_products'].find_one({"_sid":_sid})["product_list"]
		scoreSortedProductList =  userDbProducts[:20]
	else:
		# try:
		# 	if session['category'] != category:
		# 		session['category'] = category
		# 		return redirect("/browse/" + category, code=302)
		# except:
		# 	return redirect("/browse/" + category, code=302)
		try:
			_sid = session['_sid']
		except:
			app.logger.error("Issue in storing session Sev-2")
			responseDict['status'] = {'code':400,'desc':'Session Issue'}
			# return redirect("/browse/" + category, code=302)
		userDbProducts = mongoUserVariables['listing_products'].find_one({"_sid":_sid})["product_list"]
		scoreSortedProductList = userDbProducts[:start+20]
	productList = []
	for prod in scoreSortedProductList:
		prodDetail = {}
		prodDetail = getProductDetail(prod['product_id'])
		
		if len(prodDetail['priceList']['priceList']) != 0 and prodDetail['min_priceDict']:

			productList.append(prodDetail)
	
	totalProducts = len(userDbProducts)
	responseDict['start'] = start
	responseDict['status'] = {'code':200}
	responseDict['productList'] = productList
	responseDict['category'] = category
	responseDict['totalProducts'] = totalProducts
	return responseDict


@mod.route('/search', methods=['GET'], strict_slashes=False)
def search():
	category = "all"
	queryText = request.args.get('q')

	category_product_list = 'product_list'
	try:
		start = int(request.args.get('start'))
	except:
		start = None 
	if not start:
		start = 0		
		curr_dir =  os.path.realpath(os.path.dirname(__file__))
		whoosh_dir = curr_dir + "/../warehouse/index"
		productNameIndex = open_dir(whoosh_dir)
		
		query = QueryParser("productname", schema=productNameIndex.schema).parse(queryText)

		productSearchList = []
		with productNameIndex.searcher() as searcher:
			results = searcher.search(query, limit=None)
			productSearchList = [result["nid"] for result in results]
		productSearchList = list(set(productSearchList))
		
		productList= productSearchList
		category = request.args.get('category')
		if category:
			productList = [prod for prod in productList if getProductMasterInfo(prod)['category'] == category]
		session[category_product_list] = productList
		totalProducts = len(session[category_product_list])
		productList =  session[category_product_list][:20]
	else:
		totalProducts = len(session[category_product_list])
		productList = session[category_product_list]
		category = request.args.get('category')
		if category:
			productList = [prod for prod in productList if getProductMasterInfo(prod)['category'] == category]		
		productList = session[category_product_list][0:start+20]
	app.logger.info("Query Text: " + str(queryText))
	productList = [getProductDetail(prod) for prod in productList]
	title = "Bazaarfunda: Searching for " + queryText
	if category:
		title = title + " in " + category
	return render_template("search.html",allCategories=g.allCategories, query=queryText,
	 productList=productList, start=start,totalProducts=totalProducts,
	 category=category, cartDetails=g.cartDetails, all_cat_details = g.all_cat_details, recoCategory=g.recoCategory, title=title)


@mod.route('/product-search', methods=['GET'], strict_slashes=False)
@jsonResponse
def productSearchAutoComplete():
	category = getArgAsList(request, 'category')[0]
	qu = getArgAsList(request, 'qu')[0]
	if category:
		category = "all"
	print len(qu), qu
	if len(qu) < 4:
		return []
	else:
		return getProductAutoCompleteList(category, qu)
	
@app.errorhandler(404)
def not_found(error):
	g.cartDetails = [getProductDetail(product_id) for product_id in getCartDetails()]
	allCategoryCursor = mongoCategoryDetails.find()
	allCategoriesDict = {}
	for doc in allCategoryCursor:
		allCategoriesDict[doc['type']] = doc	
	g.all_cat_details = allCategoriesDict	
	title = "Bazaarfunda: Oops!! You landed on no man's land."
    	return render_template("404.html", cartDetails=g.cartDetails, title = title, all_cat_details = g.all_cat_details)

@app.errorhandler(500)
def internal_error(error):
	g.cartDetails = [getProductDetail(product_id) for product_id in getCartDetails()]
	allCategoryCursor = mongoCategoryDetails.find()
	allCategoriesDict = {}
	for doc in allCategoryCursor:
		allCategoriesDict[doc['type']] = doc	
	g.all_cat_details = allCategoriesDict
    	title = "Bazaarfunda: Oops!! You landed on no man's land."
    	# return render_template('404.html'), 404
    	return render_template("404.html", cartDetails=g.cartDetails, title = title, all_cat_details = g.all_cat_details)
    	# return jsonify(status = "Page Not Found"), 404


# This method provides the category filter that are checked to be shown on the left sode of the listing page
def getCategoryFilterCheckedStatus():
	categoryFilterCheckedStatus = {}
	for filterItem in request.args:
		itemCheckStatus = {}
		if filterItem == 'price':
			priceItems = request.args[filterItem].split(',')
			priceItems = [pItems.split('_') for pItems in  priceItems]

			try:
				priceItems = [item for sublist in priceItems for item in sublist]
				priceItems = [int(item) for item in  priceItems]
				priceItems.sort()
				priceItems = [priceItems[0], priceItems[-1]]
			except:
				priceItems = []			
			categoryFilterCheckedStatus[filterItem] = priceItems
		else:
			for item in request.args[filterItem].split(','):
				itemCheckStatus[item] = True		
			categoryFilterCheckedStatus[filterItem] = itemCheckStatus
	return categoryFilterCheckedStatus

# This method provides the banner and hot and top brands wagera static details for the listing page
def getListingStatic(category):
	listingStatic = getListingPageCategoryDict(category,'listing')
	try:		
		for idx, compItems in enumerate(listingStatic['compareitems']):
			listingStatic['compareitems'][idx]['linkName'] = getProductMasterInfo(compItems['link'])['product_name']
			listingStatic['compareitems'][idx]['locationName'] = getProductMasterInfo(compItems['location'])['product_name']
	except:
		listingStatic['compareitems'] = []
	try:
		for idx, killerItems in enumerate(listingStatic['killer']):
			listingStatic['killer'][idx]['product'] = getProductDetail(killerItems['link'])
			listingStatic['killer'][idx]['discount'] = killerItems['location']
	except:
		listingStatic['killer'] = []

	try:
		for custom_section in listingStatic['custome_item_list']:
			listingStatic['custome_item_list'][custom_section] = [getProductDetail(pid) for pid in listingStatic['custome_item_list'][custom_section]]		
	except:
		pass

	try:
		#TODO : Split the link and the location
		for custom_section in listingStatic['custome_link_list']:
			print custom_section
	except:
		pass

	try:
		listingStatic['most_reviewed'] = [getProductDetail(pid) for pid in listingStatic['most_reviewed']]
	except:
		pass

	return listingStatic

def urlToDict():
	urlImmDict = request.args
	ImmDict = urlImmDict.copy().to_dict()
	
	urlDict = {}
	for key in urlImmDict:
		value = urlImmDict[key].split(',')
		try:
			value.remove('')
		except:
			pass
		if len(value) != 0:
			urlDict[key] = value
	return urlDict



		
