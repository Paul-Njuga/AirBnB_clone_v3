#!/usr/bin/python3
"""Blueprints"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Returns status of the API"""
    return jsonify({'status': 'OK'})
