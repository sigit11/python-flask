"""
Routes and views for the flask application.
"""
from flask import render_template, g, make_response, request, Flask, redirect, url_for, abort
from flask.json import jsonify
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS
from Sigit import app

import json
import datetime


CORS(app)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return "This is a home page that you asked for !"
