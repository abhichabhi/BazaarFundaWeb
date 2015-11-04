from app import mongoProductmaster, mongoProductSpecification, mongoProductPrice, mongoKeywords, mongoReviews, mongoProductCompareReco, mongoProductReco, mongoFilterSpecificationDB, mongoScores,mongoProductOverridePrice
import traceback, time
from random import shuffle
from operator import itemgetter
from lockSync import getProductIdResults
from multiprocessing.pool import ThreadPool

pool_size = 30  # to parallelize bulk Data aggregators"
pool = ThreadPool(pool_size)

'''
methods for obtaining single product details
'''
def getProductMasterInfo(product_id):
	return mongoProductmaster.find_one({'product_id':product_id})

def getProductSpecification(product_id):
	return mongoProductSpecification.find_one({'product_id':product_id})

def getProductPrice(product_id):
	product_price =  mongoProductPrice.find_one({'product_id':product_id})
	try:
		priceList = product_price['priceList']
	except:
		priceList = []
	min_priceDict = {}
	override_Price = mongoProductOverridePrice.find_one({'product_id':product_id})
	if priceList:
		min_price = 100000000		
		for price in priceList :
			if override_Price:
				override_Price_Dict = override_Price['override_price']
				override_website_price = None
				try:
					override_website_price = override_Price_Dict[price['website']]
				except:
					override_website_price = None
				if override_website_price:
					price['price'] = override_website_price
			if price['price'] < min_price and price['price'] != 0:
				min_price = price['price']
				min_priceDict = price
	return product_price, min_priceDict

def getProductReviews(product_id):
	rating = {}
	try:
		rating = mongoReviews.find_one({'product_id':product_id})
	except:
		pass
	return rating

def getProductRating(product_id):
	product_RatingCursor = mongoKeywords.find({'product_id':product_id})
	ratingDict = []
	try:
		for product_Rating in product_RatingCursor:
			ratingDict.append(product_Rating)
	except:
		pass		
	return ratingDict

def getProductScores(product_id):
	product_Rating = mongoScores.find_one({'product_id':product_id})
	return product_Rating['score']

def threadedProductDetail(product_id):
	product = {}
	# product['specification'] =  getProductIdResults(getProductSpecification, product_id)
	product['rating'] =  getProductIdResults(getProductRating, product_id)
	# product['review'] =  getProductIdResults(getProductReviews, product_id)
	# product['reco'] =  getProductIdResults(getProductReco, product_id)
	product['master'] =  getProductIdResults(getProductMasterInfo, product_id)
	product['priceList'], product['min_priceDict'] = getProductIdResults(getProductPrice, product_id)
	return product

def getProductDetail(product_id):
	product = {}
	product['specification'] = getProductSpecification(product_id)
	product['priceList'], product['min_priceDict'] = getProductPrice(product_id)
	product['rating'] = getProductRating(product_id)

	finalrating = 0.00
	try:
		
		finalrating = getProductScores(product_id)['overall']['finalRating']
	except:
		pass
	
	product['finalrating'] = "{0:.2f}".format(round(finalrating,2))
	product['review'] = getProductReviews(product_id)
	product['reco'] = getProductReco(product_id)
	product['master'] = getProductMasterInfo(product_id)
	return product

def getProductAutoCompleteList(category):
	
	if category is not "all":
		
		allProducts = mongoProductmaster.find({'category':category})
	else:
		
		allProducts = mongoProductmaster.find()
	productList = []
	for products in allProducts:
		producDict = {}
		producDict['name'] = products['product_name']
		producDict['type'] = products['category']
		producDict['icon'] = "https://s3-ap-southeast-1.amazonaws.com/bazaarfunda/Website/static/ProductImage/" + products['product_id'] + ".jpg"
 		productList.append(producDict)
 	return productList

def getProductReco(product_id):
	try:
		allRecoProducts = mongoProductReco.find_one({'product_id':product_id})['recommendedProducts']		
		allRecoProducts = list(set(allRecoProducts))
		allRecoProducts.remove("")		
		allRecoProducts = allRecoProducts[:10]
		
	except Exception, err:
		allRecoProducts = []	

	try:
		allCompareRecoProducts = mongoProductCompareReco.find_one({'product_id':product_id})['recommendedProducts']
		allCompareRecoProducts = list(set(allCompareRecoProducts))
		allCompareRecoProducts.remove("")
		allCompareRecoProducts = allCompareRecoProducts[:5]
	except Exception, err:
		allCompareRecoProducts = []
	shuffle(allRecoProducts)
	shuffle(allCompareRecoProducts)
	recoDict = {}
	recoDict['allComp'] = [getProductMasterInfo(p_id) for p_id in allCompareRecoProducts]
	allRecoList = [] 
	for p_id in allRecoProducts:
		product = {}
		product['master'] = getProductMasterInfo(p_id)
		product['min_price'] = getProductPrice(p_id)[1]
		allRecoList.append(product)
	recoDict['allReco'] = allRecoList
	return recoDict

def getFilteredProductSpecification(requestQuery, category):
	inStr = '$in'
	requestQuery = requestQuery.copy().to_dict()
	# print requestQuery, "in getFilteredProductSpecification"
	try:
		del requestQuery['price']
	except:
		pass
	try:
		del requestQuery['keywords']
	except:
		pass
	try:
		del requestQuery['weights']
	except:
		pass
	try:
		del requestQuery['reco']
	except:
		pass
	queryStr = {}
	for param in requestQuery:
		paramDict = {}
		paramDict[inStr] = requestQuery[param].split(',')
		queryStr[param] = paramDict
	
	produCursor = mongoFilterSpecificationDB[category].find(queryStr)	
	prodList = [prod['product_id'] for prod in produCursor]
	return prodList


def getFilteredProductPriceRange(pRange, category):
	productIdRegex = '^' + category[0].capitalize()
	
	# 'priceList.price':{'$gt':pRange[0],'$lt':pRange[1]},
	if pRange:
		pProducts = mongoProductPrice.find({'priceList.price':{'$gt':pRange[0],'$lt':pRange[1]},'product_id': {'$regex':productIdRegex}})
	else:
		pProducts = mongoProductPrice.find({'product_id': {'$regex':productIdRegex}})
	pProducts = [prod['product_id'] for prod in pProducts]
	return pProducts

def getScoreSortedProductID(product_list, category, keywords, weights):
	# millis = lambda: int(round(time.time() * 1000))
	# print product_list, "in getScoreSortedProductID########"
	scoreList = []

	for prod in product_list:
		# async_result = pool.apply_async(getProductScore, (prod, category,keywords,weights,))
		product_score = getProductScore(prod, category,keywords,weights)
		# product_score = async_result.get()
		if product_score != None:
			scoreList.append(product_score)
	# scoreList = [getProductScore(prod, category) for prod in product_list if getProductScore(prod, category) != None]

	scoreList = sorted(scoreList, key=itemgetter('score'), reverse=True)
	return scoreList
	

def getProductScore(product_id, category,user_keywords,weights):	
	allKeywords = getProductScores(product_id)
	score = 0
	scoreCount = 0
	weightFlag = 0
	weightDividend = 1

	if weights:
		weightDividend = 0
	 	for weight in weights:
	  		weightDividend = weightDividend + int(weight)
	user_key_score = 0
	if user_keywords:
		for user_keyword in user_keywords:
			
			try:
				scoreCount = scoreCount + 1
				key_score = allKeywords[user_keyword] ['finalRating']
				
				if weightFlag:
 					key_score = key_score*weights[user_keywords.indexof(user_keyword)]
			except:
				key_score = 0
			
 			user_key_score = user_key_score + key_score
 	else:
 		scoreCount = 1
 		user_key_score = allKeywords['overall'] ['finalRating']
 	user_key_score = user_key_score/scoreCount

 	user_key_score = user_key_score/weightDividend
 	user_overall_score = allKeywords['overall'] ['finalRating']
 	user_key_score = round(user_key_score,2)
 	user_overall_score = round(user_overall_score,2)
 	# print user_key_score
 	return {'product_id':product_id, 'score': user_key_score, "overall_score": user_overall_score}
	 	