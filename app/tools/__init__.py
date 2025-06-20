from flask import Blueprint
tools_bp = Blueprint('api_endpoints', __name__)
from .routes.routes import *