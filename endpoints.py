"""File used to register endpoints."""
from flask import Blueprint, jsonify
from flask_cors import CORS

api_v2 = Blueprint('api_v2', __name__)


@api_v2.route('/api/v2/auth', methods=['GET'])
def home():
    """Directs to the landing page of the application"""
    return jsonify({"message": "Welcome to my home page"})
