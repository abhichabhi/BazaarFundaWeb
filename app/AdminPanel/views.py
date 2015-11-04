from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from bson.objectid import ObjectId
from pymongo import ASCENDING
from bson import json_util
import json
from app import mongoAdminDB as mongo
import functools
from app import app, mongoProductOverridePrice
from app.decorators import mongoJsonify, jsonResponse

from app.util import getArgAsList
mod = Blueprint('banners', __name__, url_prefix='/admin')
def get_locale():
	try:
		language = getArgAsList(request, 'lang')[0]
	except:
		language = 'hi'
	print request.accept_languages.best_match(LANGUAGES.keys())
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

	listing = mongo.listing.find_one()
	categoryList = [cat for cat in listing]
	categoryList.pop()
	try:
		categoryListing = listing[category]		
	except:
		categoryListing = listing['dummy']

	compareitems = categoryListing['compareitems']
	hotbrands = categoryListing['hotbrands']
	economicbrands = categoryListing['economicbrands']
	topbanner = categoryListing['topbanner']
	right_vertical = categoryListing['right_vertical_aff']
	killerDeals = categoryListing['killer']
	most_reviewed = categoryListing['most_reviewed']
	
	return render_template('admin/listing.html', title="Listing banner : " + category,
		category=category,categoryList=categoryList, compareitems=compareitems,
		 hotbrands=hotbrands,economicbrands=economicbrands,
		topbanner=topbanner,killerDeals=killerDeals,most_reviewed=most_reviewed, right_vertical=right_vertical)

@mod.route('/banner/listing/submit', methods=['GET','PUT'])
def listingFormSubmit():
	if request.method == 'PUT':
		respData =json.loads(request.data)
		category = respData['category']
		data = respData['data']
		print data
		print category
	listing = mongo.listing.find_one()
	listing[category] = data
	updateCollection("listing", listing)
	return "Listing form submitted successfully"

@mod.route('/priceoverride/<product_id>', methods=['GET','PUT'])
@login_required
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
	return mongo[page].find_one()[category]

def getHomePageDict():
	return mongo.home.find_one()
