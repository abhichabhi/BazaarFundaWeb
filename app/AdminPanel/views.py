from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from bson.objectid import ObjectId
from pymongo import ASCENDING
from bson import json_util
import json
from app import mongoAdminDB as mongo, mongoCategoryDetails
import functools
from app import app, mongoProductOverridePrice
from app.decorators import mongoJsonify, jsonResponse
from app.util import getArgAsList
from bson import json_util

mod = Blueprint('banners', __name__, url_prefix='/admin')
def get_locale():
	try:
		language = getArgAsList(request, 'lang')[0]
	except:
		language = 'hi'
	return language

@mod.route('/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('password'):
        password = request.form.get('password')
        # TODO: If using a one-way hash, you would also hash the user-submitted
        # password and do the comparison on the hashed versions.
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect('/admin/')
        else:
            flash('Incorrect password.', 'danger')
    return render_template('admin/login.html', next_url=next_url)

@mod.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('.login'))
    return render_template('admin/logout.html')

def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('.login', next=request.path))
    return inner

@mod.route('/', methods=['GET'])
@login_required
def AdminIndex():
	return render_template('admin/AdminIndex.html')

@mod.route('/category/catType', methods=['GET'])
def catType():
	try:
		category= getArgAsList(request, 'category')[0]
	except:
		category = 'new'

	listing = mongoCategoryDetails.find()
	categoryList = [li['type']  for li in listing]

	catTypeCursor =  mongoCategoryDetails.find()
	catType = [cat for cat in catTypeCursor]

	if category != 'new':
		listingJSON = mongoCategoryDetails.find_one({'type':category})
	else:
		listingJSON = ""
	listingJSON = json.dumps(listingJSON)

	return render_template('admin/catType.html', catType=catType,
	 categoryList=categoryList, listingJSON=listingJSON,category=category)

@mod.route('/category/catType/submit', methods=['PUT'])
def catTypeSubmit():
	if request.method == 'PUT':
		respData =  request.get_json(silent=True)
		# respData =json.loads(request.json)
		for data in respData:
			category =  data
			catJSON = respData[category]
		print catJSON
		catJSON = json.loads(catJSON)
		try:
			catJSON['type']
			print "type present"
			try:
				listingJSON = mongoCategoryDetails.find_one({'_id':catJSON['_id'], 'type': catJSON['type']})
				mongoCategoryDetails.save(catJSON)
				return "Saved new document"
			except:
				
				mongoCategoryDetails.save(insert)
				return "new document"
		except:			
			mongoCategoryDetails.delete_one({'_id':catJSON['_id']})
			return "Type not present, so delete this entry of category"
	return "Submitted Successfully"

@mod.route('/banner/home/', methods=['GET'])
@login_required
def homeForm():
	home = mongo.home.find_one()
	TopParallax = home["TopParallax"]
	BottomParallax = home["BottomParallax"]
	Sliderbanner = home["NewProducts"]
	MediaPublication = home["MediaPublication"]
	title = "Banners of home page"
	return render_template("admin/homepage.html", TopParallax=TopParallax, BottomParallax=BottomParallax, Sliderbanner=Sliderbanner, MediaPublication=MediaPublication, title = title)

@mod.route('/banner/home/submit', methods=['GET'])
def homeFormSubmit():
	TopParallax = getArgAsList(request, 'TBanner')[0]
	BottomParallax = getArgAsList(request, 'PBanner')[0]
	Sliderbanner = getArgAsList(request, 'sliderBanner')
	MediaLink = getArgAsList(request, 'MediaLink')[0]
	MediaBanner = getArgAsList(request, 'MediaBanner')[0]
	MediaDict = {"location":MediaBanner, "link":MediaLink}
	home = mongo.home.find_one()
	if TopParallax == "":
		TopParallax = home["TopParallax"]
	if BottomParallax == "":
		BottomParallax = home["BottomParallax"]
	if Sliderbanner == []:
		Sliderbanner = home["Sliderbanner"]
	MediaPublication = home["MediaPublication"]
	if MediaLink != "" and MediaBanner != "":
		MediaPublication.append(MediaDict)
	homeBannerDict = {"_id":home["_id"], "TopParallax":TopParallax, "BottomParallax":BottomParallax,"NewProducts":Sliderbanner, "MediaPublication":MediaPublication}
	updateCollection("home", homeBannerDict)
	return "Listing form submitted successfully"

@mod.route('/banner/listing', methods=['GET'])
@login_required
def listingForm():
	try:
		category= getArgAsList(request, 'category')[0]
	except:
		category = 'new'
	print category


	listing = mongoCategoryDetails.find()
	categoryList = [li['type'][:-1] if li['type'].endswith('s') else li['type']  for li in listing]
	print categoryList
	# for cat in categoryList:
	# 	if cat.endswith('s'):
	# 		cat = cat[:-1]

	admin_properties = mongo.listing.find_one()
	try:
		categoryListing = admin_properties[category]		
	except:
		pass
		# categoryListing = listing['dummy']
	try:
		compareitems = categoryListing['compareitems']
	except:
		compareitems = []
	try:
		hotbrands = categoryListing['hotbrands']
	except:
		hotbrands = []
	try:
		economicbrands = categoryListing['economicbrands']
	except:
		economicbrands = []
	try:
		topbanner = categoryListing['topbanner']
	except:
		topbanner = []
	try:
		right_vertical = categoryListing['right_vertical_aff']
	except:
		right_vertical = []
	try:
		killerDeals = categoryListing['killer']
	except:
		killerDeals = []
	try:
		most_reviewed = categoryListing['most_reviewed']
	except:
		most_reviewed = []
	try:
		custom_product_list = categoryListing['custome_item_list']
	except:
		custom_product_list = []

	try:
		custom_link_list = categoryListing['custom_link_list']
	except:
		custom_link_list = []
	print custom_link_list
	
	return render_template('admin/listing.html', title="Listing banner : " + category,
		category=category,categoryList=categoryList, compareitems=compareitems,
		 hotbrands=hotbrands,economicbrands=economicbrands,
		topbanner=topbanner,killerDeals=killerDeals,most_reviewed=most_reviewed, right_vertical=right_vertical, custom_product_list=custom_product_list, custom_link_list=custom_link_list)

@mod.route('/banner/listing/submit', methods=['GET','PUT'])
def listingFormSubmit():
	if request.method == 'PUT':
		respData =json.loads(request.data)
		category = respData['category'].replace('%20',' ')
		data = respData['data']
		print data['custome_item_list'], category
		# data['custome_item_list'] = {}
		print data
		print category
	listing = mongo.listing.find_one()
	listing[category] = data
	updateCollection("listing", listing)
	return "Listing form submitted successfully"

@mod.route('/priceoverride/<product_id>', methods=['GET','PUT'])
# @login_required
def priceOverride(product_id):
	if request.method == 'GET':	
		return render_template('admin/priceOverride.html', product_id=product_id)
	if request.method == 'PUT':
		productDoc = {}
		respData = json.loads(request.data)
		if respData['override_price']:
			productDoc['product_id'] = product_id
			productDoc['override_price'] = respData['override_price']
			document = mongoProductOverridePrice.find_one({'product_id':product_id})			
			if document:
				productDoc["_id"] = document["_id"]
				mongoProductOverridePrice.save(productDoc)
			else:
				mongoProductOverridePrice.insert(productDoc)
		return "Listing form submitted successfully"
			

def updateCollection(collection, dict):
	print mongo[collection].save(dict)

def getListingPageCategoryDict(category,page):
	if category == 'tablets':
		category = 'tablet'
	if category == 'mobiles':
		category = 'mobile'
	try:
		return mongo[page].find_one()[category]
	except:
		return {}

def getHomePageDict():
	return mongo.home.find_one()

# def mongoSaveDocument(document,collection, client, identifier, versionControl=False):
# 	# print identifier
# 	collectionOriginal = client[collection]
# 	if versionControl==True:
# 		versioned_collection = collection + "v_1_0"
# 		collection_1_0 = client[versioned_collection]
# 		collection_1_0.remove()
# 		for record in collectionOriginal.find():
# 			collection_1_0.insert(record)
#     	    mongoSaveDocument(document,collection, client, identifier, False)
#     else:
# 		collectionOriginal = client[collection]
# 		priceDoc = collectionOriginal.find_one({identifier:document[identifier]})
# 		if priceDoc:
# 			document["_id"] = priceDoc["_id"]
# 			collectionOriginal.save(document)
# 		else:
# 			collectionOriginal.insert(document)   
