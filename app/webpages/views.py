from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from app import app
from app import mongoCategoryDetails, categoryListingFilter
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
from app import mongoCategoryDetails
from flask.ext.social import Social

mod = Blueprint('webpage', __name__, url_prefix='')

app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': '1435721096655907',
    'consumer_secret': '1f8fb8b82f3e84030274a6e9a368b91b'
}

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


@mod.route('/',methods=['GET'], strict_slashes=False)
def home():
	title = "Bazaarfunda: Discover Products that suits your needs. Compare products and prices"
	allCategories = mongoCategoryDetails.find()
	allCategories = [cat['type'] for cat in allCategories]
	allRecentProducts = getHomePageDict()['NewProducts']
	allRecentProducts = [getProductDetail(product_id) for product_id in allRecentProducts]
	allMediaPublication = getHomePageDict()['MediaPublication']
	category = "all"
	return render_template("landingpage.html", allCategories=allCategories, allRecentProducts=allRecentProducts,
		category=category,cartDetails=g.cartDetails, all_cat_details = g.all_cat_details,allMediaPublication=allMediaPublication,title=title)

@mod.route('/compare',methods=['GET'], strict_slashes=False)
def compare():
	cartDetails=g.cartDetails
	category = None
	categoryDetails = None
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
	 categoryDetails=categoryDetails, category=category, all_cat_details = g.all_cat_details, title = title)


@mod.route('/pdp/<product_id>/<slug>', methods=['GET'], strict_slashes=False)
@mod.route('/pdp/<product_id>', defaults={'slug': None}, methods=['GET'], strict_slashes=False)
def productDetail(product_id, slug=None):
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
		category=category, all_cat_details = g.all_cat_details, title = title)

@mod.route('/browse/<category>', methods=['GET'], strict_slashes=False)
def browse(category):
	filterFlag = 0	
	categoryFilterCheckedStatus = getCategoryFilterCheckedStatus()
	listingStatic = getListingStatic(category)
	urlDict = urlToDict()
	millis = lambda: int(round(time.time() * 1000))
	reco_bool = 0
	try:
		start = int(request.args.get('start'))
	except:
		start = None 
		scoreSortedProductList = []

	if not start:
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
		if 'reco' in urlDict:
			reco_bool = 1
		priceProductIdList = getFilteredProductPriceRange(priceRange, category)		
		finalProductList = list(set(priceProductIdList) & set(specProductIdList))		
		scoreSortedProductList = getScoreSortedProductID(finalProductList,category, keywords, weights)
		session['product_list'] = scoreSortedProductList	
		# print session['product_list'], "without start"
		scoreSortedProductList =  session['product_list'][:20]
	else:
		print session['product_list'], "with start"
		scoreSortedProductList = session['product_list'][0:start+20]
	productList = []
	for prod in scoreSortedProductList:
		prodDetail = {}
		prodDetail = getProductDetail(prod['product_id'])
		# prodDetail['finalrating'] = prod['score']
		productList.append(prodDetail)
	
	totalProducts = len(session['product_list'])
	if len(categoryFilterCheckedStatus) == 0:
		filterFlag = 1
	categoryFilter = categoryListingFilter[category]
	title = "Bazaarfunda: "
	if 'keywords' in urlDict:
		title = title + "Best Recommended " + category + " acording to your needs"
	else:
		title = title + "Get the best " + category + " according to other customers"
	return render_template("listing_small_prev.html", categoryFilter=categoryFilter,
	 categoryFilterCheckedStatus=categoryFilterCheckedStatus, listingStatic=listingStatic,
	 filterFlag=filterFlag, category=category, cartDetails=g.cartDetails,
	 productList=productList, totalProducts=totalProducts, start=start,
	  all_cat_details = g.all_cat_details, reco_bool=reco_bool, title = title)

@mod.route('/search', methods=['GET'], strict_slashes=False)
def search():
	allCategories = mongoCategoryDetails.find()
	allCategories = [cat['type'] for cat in allCategories]
	category = "all"
	queryText = request.args.get('q')
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
		session['product_list'] = productList
		totalProducts = len(session['product_list'])
		productList =  session['product_list'][:20]
	else:
		totalProducts = len(session['product_list'])
		productList = session['product_list']
		category = request.args.get('category')
		if category:
			productList = [prod for prod in productList if getProductMasterInfo(prod)['category'] == category]		
		productList = session['product_list'][0:start+20]
	productList = [getProductDetail(prod) for prod in productList]
	title = "Bazaarfunda: Searching for " + queryText
	if category:
		title = title + " in " + category
	return render_template("search.html",allCategories=allCategories, query=queryText,
	 productList=productList, start=start,totalProducts=totalProducts,
	 category=category, cartDetails=g.cartDetails, all_cat_details = g.all_cat_details,title=title)


@mod.route('/product-search', methods=['GET'], strict_slashes=False)
@jsonResponse
def productSearchAutoComplete():
	category = getArgAsList(request, 'category')[0]
	if category:
		category = "all"
	return getProductAutoCompleteList(category)
	
	# if category:
	# 	return getProductAutoCompleteList(category)
	# else:
	# 	return getProductAutoCompleteList()

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
	for idx, compItems in enumerate(listingStatic['compareitems']):
		listingStatic['compareitems'][idx]['linkName'] = getProductMasterInfo(compItems['link'])['product_name']
		listingStatic['compareitems'][idx]['locationName'] = getProductMasterInfo(compItems['location'])['product_name']

	for idx, killerItems in enumerate(listingStatic['killer']):
		listingStatic['killer'][idx]['product'] = getProductDetail(killerItems['link'])
		listingStatic['killer'][idx]['discount'] = killerItems['location']

	listingStatic['most_reviewed'] = [getProductDetail(pid) for pid in listingStatic['most_reviewed']]

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



		
