#!/usr/bin/python3
"""View for Place objects that handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models import storage
