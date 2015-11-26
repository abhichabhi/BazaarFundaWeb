from flask import Flask, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from util import install_secret_key
import os
from playhouse.flask_utils import FlaskDB
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
APP_DIR = os.path.dirname(os.path.realpath(__file__))
ADMIN_PASSWORD = 'secret'
SITE_WIDTH = 800
app = Flask(__name__)
app.config.from_object(__name__)
formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler('/var/log/apache2/bazaarfunda.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.info("Initiating app")
''' To check if the route is working '''

@app.route('/hello',methods=['GET'])
def hello():
    return "Hello"

if not app.config['DEBUG']:
    install_secret_key(app)

'''
Initialize various mongo db clients with collection
'''
#AllProduct client
mongoProductmaster = MongoClient('localhost', 27017)['Productmaster']['allproducts']
#Price db
mongoProductPrice = MongoClient('localhost', 27017)['ProductPrice']['allProducts']
#Override PriceDB
mongoProductOverridePrice = MongoClient('localhost', 27017)['ProductPrice']['override']
#Specification
mongoProductSpecification = MongoClient('localhost', 27017)['ProductSpecification']['allproducts']
#KeywordRatings
mongoKeywords = MongoClient('localhost', 27017)['Productratings']['keywords']
#Score
mongoScores = MongoClient('localhost', 27017)['Productratings']['scores']
#Keyword Reviews
mongoReviews = MongoClient('localhost', 27017)['Productratings']['reviews']
#categoryDetails

#FilterSpecification
mongoFilterSpecificationDB = MongoClient('localhost', 27017)['SpecificationFilter']

mongoCategoryDetails = MongoClient('localhost', 27017)['categoryDB']['catType']
#category Reco Filters
mongoCategoryRecoFilter = MongoClient('localhost', 27017)['categoryDB']['RecoFilter']
#category Listing Filters
categoryListingFilter = MongoClient('localhost', 27017)['categoryDB']['ListingFilter'].find_one()
#ProductReco
mongoProductReco = MongoClient('localhost', 27017)['ProductRecommendation']['allReco']
#ProductCompareReco
mongoProductCompareReco = MongoClient('localhost', 27017)['ProductRecommendation']['allComp']
#Admin DB
mongoAdminDB = MongoClient('localhost', 27017)['interstellerDB']

#User Variables
mongoUserVariables = MongoClient('localhost', 27017)['userVariables']
try:
	mongoUserVariables['listing_products'].ensure_index("date", expireAfterSeconds=3600000) 
except:
	pass
'''
various modules
'''
#Web PageModule
#WebPages Views
from app.webpages.views import mod as webModule
app.register_blueprint(webModule)

from app.AdminPanel.views import mod as adminModule

app.register_blueprint(adminModule)

from app.Downloads.views import mod as downloadModule

app.register_blueprint(downloadModule)

from app.cart.views import mod as cartModule

app.register_blueprint(cartModule)

from app.restfull.views import mod as restModule

app.register_blueprint(restModule)

#Blog ke chochde
# The `database` is the actual peewee database, as opposed to flask_db which is
# the wrapper.
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'blog.db')
app.config['DATABASE'] = DATABASE
flask_db = FlaskDB(app)
database = flask_db.database

# #Blog Views
# from app.blog.views import mod as blogModule
# from app.blog.views import Entry, FTSEntry
# database.create_tables([Entry, FTSEntry], safe=True)
# app.register_blueprint(blogModule)
