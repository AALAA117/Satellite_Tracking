#!/usr/bin/python3
"""
initilization package
"""
from flask import Blueprint

main = Blueprint('main', __name__, url_prefix='/api')

from api.route.satellite import *
