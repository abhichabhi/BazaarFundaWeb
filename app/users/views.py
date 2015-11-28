from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from werkzeug import check_password_hash, generate_password_hash
from pymongo import MongoClient
# from app import db
# from app.users.forms import RegisterForm, LoginForm
# from app.users.models import User
# from app.users.decorators import requires_login
# from app import mongo
from app import app
from app.decorators import mongoJsonify, jsonResponse
import logging
from app.util import getArgAsList
from logging.handlers import RotatingFileHandler
import datetime

mod = Blueprint('users', __name__, url_prefix='/users')

@mod.route('/subscribePrice', methods=['GET', 'POST'])
@jsonResponse
def subscribePrice():
  email = getArgAsList(request, 'email')[0]
  # productName = getArgAsList(request, 'productName')[0]
  productId = getArgAsList(request, 'productId')[0]
  priceCutOff = getArgAsList(request, 'priceCutOff')[0]
  mongo = MongoClient('localhost', 27017)['userRequests']
  priceSubscribers = mongo.priceSubscribers
  existEntry = priceSubscribers.find_one({'email':email,'priceCutOff':priceCutOff,'status':'A'})
  app.logger.info(existEntry)
  if not existEntry:
    update_time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    priceSubscribers.insert({
    "email" : email,
    "productId" : productId,
    "priceCutOff" : priceCutOff,
    "status" : 'A',
    "date": update_time
  })
    return True
  else:
    return False

