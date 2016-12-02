"""
Routes and views for the flask application.
"""
from flask import render_template, g, make_response, request, Flask, redirect, url_for, abort
from flask.json import jsonify
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS
from Sparse import app

import json
import redis
import MySQLdb
import datetime

"""
Redis Init
"""
try:
    redisServer = redis.StrictRedis(host = '127.0.0.1', port = 6379, db = 5, password = "")
except:
    print('Redis Connection Error')

"""
Import Classes and Init Classes
"""
from Sparse.classes.common.dbconnector import dbconnector
dbObj = dbconnector(source='127.0.0.1', username = 'root', password = '',dbname = 'sparse')

from Sparse.classes.common.auth import auth
authObj = auth('secretkey', algorithm = 'HS512')

from Sparse.classes.account.users import users
userObj = users(authObj, redisServer)

from Sparse.classes.recommendation.RecomEngine import RecomEngine
recomObj = RecomEngine(redisServer)

from Sparse.classes.recommendation.RecomPlacement import RecomPlacement
recomPlacementObj = RecomPlacement(redisServer)

from Sparse.classes.search.SearchEngine import SearchEngine
searchObj = SearchEngine(redisServer)

"""
Init Auth System
"""
auth  = HTTPTokenAuth('JWT')

@auth.verify_token
def verify_token(token):
    tokenDecode = authObj.decode(token)
    if tokenDecode is False:
        return False
    else:
        g.token = token
        g.decoded = tokenDecode
        return True

"""
function of MySQL connection
"""
#def connectDB(f):
#    def func_connectDB():
#        g.db = dbObj.db_connect()
#        return True
#    return func_connectDB

"""
Application Routing
"""

CORS(app)

@app.before_request
def begin_request():
    #print('Request Start')
    g.db = dbObj.db_connect()

@app.after_request
def after_request(response):
    #print('Request End')
    return response

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return "This is a home page that you asked for !"

"""
Users Routes
"""

@app.route('/api/v1/users/login', methods = ['POST'])
def user_login():
    userAuthInfo = {
        'email' : request.json['email'],
        'password' : request.json['password']
    }
    reData = userObj.user_login(g.db, userAuthInfo)
    if reData['statusCode'] == 401:
        return jsonify({'status':reData['status']}), 401
    elif reData['statusCode'] == 500:
        return jsonify({'status':reData['status']}), 500
    elif reData['statusCode'] == 200:
        return jsonify({'status':reData['status'], 'token':reData['token']}), 200

@app.route('/api/v1/users/logout', methods = ['DELETE'])
@auth.login_required
def user_logout():
    userToken = {
        'token' : g.token
    }
    reData = userObj.user_logout(userToken)
    if reData['statusCode'] == 401:
        return jsonify({'status':reData['statusMessage']}), 401
    elif reData['statusCode'] == 500:
        return jsonify({'status':reData['status']}), 500
    elif reData['statusCode'] == 200:
        return jsonify({'status':reData['statusMessage']}), 200

@app.route('/api/v1/users', methods = ['GET'])
@auth.login_required
def recom_engine_user_detail():
    user_detail = {
        "site_name" : "sparseshop.tk",
        "site_url" : "http://sparsehop.tk",
        "username" : "Sparse Shop Admin",
        "phone" : "081384928392",
        "valid_until" : datetime.datetime.now() + datetime.timedelta(days=365),
        "subscription_level" : 5
    }
    return jsonify({'user_detail':user_detail}), 200

"""
Recommendation Routes
"""
@app.route('/api/v1/activity/recently', methods = ['GET'])
@auth.login_required
def recom_recent_activity():
    recent_activities = [
        {"time" : datetime.datetime.now() - datetime.timedelta(hours=2), "action" : "User has updated engine name from Sparshop Engine Test into Sparshop Ultimate Engine"},
        {"time" : datetime.datetime.now() - datetime.timedelta(hours=5), "action" : "User has deleted a widget"},
        {"time" : datetime.datetime.now() - datetime.timedelta(hours=10), "action" : "User has created a new widget "},
        {"time" : datetime.datetime.now() - datetime.timedelta(hours=23), "action" : "User has created a new placement"},
        {"time" : datetime.datetime.now() - datetime.timedelta(hours=48), "action" : "User has updated a placement"},
    ]
    return jsonify({'act':recent_activities}), 200

