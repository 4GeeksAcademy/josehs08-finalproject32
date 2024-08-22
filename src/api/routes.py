"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_migrate import Migrate
from api.models import db, User, Projects
from api.utils import generate_sitemap, APIException
from admin import setup_admin
from flask_cors import CORS

import requests

api = Blueprint('api', __name__)
api.url_map.strict_slashes = False


# Allow CORS requests to this API
MIGRATE = Migrate(api, db)
db.init_api(api)
CORS(api)
setup_admin(api)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/user', methods=["POST"])
def add_user():
    body = request.json

    first_name = body.get("name", None)
    last_name = body.get("last_name", None)
    username = body.get("username", None)
    email = body.get("email", None)
    password = body.get("password", None)
    role_id = body.get("role_id", None)

#get all users
@api.route('/users', methods=["GET"])
def get_all_users():
    users = User()
    users = users.query.all()
    users = list(map(lambda item: item.serialize(), users))

    return jsonify(users , 200)

# get users by id
@api.route('/user/<int:user_id>', methods=["GET"])
def get_user(user_id):
    user = User()
    user = user.query.get(user_id)

    if user is None:
        raise APIException("User not found", status_code=404)
    else: 
        return jsonify(user.serialize())
    
#add projects
@api.route('/project', methods=["POST"])
def ad_project():
    body = request.json

    name =  body.get("name", None)
    description = body.get("description", None)
    start_date = body.get("start_date", None)
    end_date = body.get("end_date", None)

# get all projects
@api.route('/puejects', methods=["GET"])
def get_all_projects():
    projects = Projects()
    projects = projects.query.all()
