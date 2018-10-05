"""Module Containing my Users"""
from datetime import datetime, timedelta

import jwt
from flask import jsonify, Blueprint
from flask_cors import cross_origin

from models import create_user, check_user_in_database, my_cursor
from Users.user_details import UserDetails

assign_my_users_routes = Blueprint("assign_my_users_routes", __name__)


@assign_my_users_routes.route('/api/v2/auth/signup', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type'])
def register():
    """Extracts user details from the post request using the UserDetails class
    imported from the user_details file. Runs a helper method called combine_details
    to check for validity of user details. uses helper function called create user
    from the models.py file fond in the root of the project to create a user and
    and inserts the user's details into the database. Otherwise it returns an error
    with an invalid message."""
    details = UserDetails()
    if details.validate_details:
        return jsonify({"message": str(details.validate_details)
                        + " must be longer then 5 and less than 60"}), 411
    if details.get_password() == details.get_password2():
        if create_user(details.get_first_name(), details.get_last_name(),
                       details.get_user_name(), details.get_email(),
                       details.get_password()) is True:
            return jsonify({"message": "Successfully registered."}), 201
        return jsonify({"message": "username or email already taken."}), 403
    return jsonify({"message": "passwords must match"}), 409


@assign_my_users_routes.route('/api/v2/auth/login', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type'])
def login():
    """Extracts user details from the post request, runs helper functions to
    confirm the user is registered, generates an access token for the user and
    responds with an appropriate message."""
    login_details = UserDetails()
    user_id = check_user_in_database(login_details.get_email(),
                                     login_details.get_password())
    if user_id:
        user_token = jwt.encode({'user': user_id[0],
                                 'exp': datetime.utcnow()
                                 + timedelta(minutes=10)},
                                "This is not the owner")
        return jsonify({"user_token": user_token.decode('utf-8'),
                        "message": "log in successful"}), 200
    return jsonify({"message": "Invalid credentials."}), 401


@assign_my_users_routes.route('/api/v2/auth/profile', methods=['GET'])
def fetch_user_profile():
    """Extracts user details from the post request, runs helper functions to
    confirm the user is registered, and fetches the user's details from the
    database."""
    details = UserDetails()
    user_id = details.get_user_id()
    if isinstance(user_id, bool) is False:
        my_cursor.execute("""SELECT FIRSTNAME, LASTNAME, USERNAME,EMAIL
                          FROM USERS WHERE ID = %s;""", (user_id,))
        one_entry = my_cursor.fetchall()
        return jsonify({"message": one_entry}), 200
    return jsonify({"message" " Invalid token please login first"}), 405
