"""Used for dealing with diary entries."""
from datetime import datetime, timedelta

import jwt
from flask import request, jsonify, Blueprint
from flask_cors import cross_origin

from models import connection, my_cursor, create_entry
from models import update_entry, remove_entry
from Entries.entry_details import UserEntries

assign_my_entries_routes = Blueprint("assign_my_entries_routes", __name__)


@assign_my_entries_routes.route('/api/v2/entries', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def add_entries():
    """Extracts user details from the post request, runs helper
    functions to confirm the user is registered, and inserts the
    user's details into the database."""
    details = UserEntries()
    user_id = details.get_user_id()
    if details.validate_details:
        return jsonify({"message": str(details.validate_details)
                        + " must be longer then 5 and less than 60"}), 411
    if isinstance(user_id, bool) is False:
        create_entry(details.get_title(), details.get_contents(),
                     details.get_date_of_event(),
                     datetime.now() + timedelta(hours=24),
                     details.get_reminder_time(), user_id)
        return jsonify({"message": "Entry is now in the database."}), 201
    return jsonify({"message": "Invalid token please login first"}), 403


@assign_my_entries_routes.route('/api/v2/entries/<int:entry_id>',
                                methods=['GET'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def get_one_entry(entry_id):
    """Extracts contents from the post request and responds with the
    entry."""
    details = UserEntries()
    user_id = details.get_user_id()
    if isinstance(user_id, bool) is False:
        my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
                          FROM ENTRIES WHERE ID = %s AND USERID = %s;""",
                          (entry_id, user_id,))
        one_entry = my_cursor.fetchone()
        if one_entry:
            return jsonify({"message": one_entry}), 200
        return jsonify({"message": "The entry does not exist"}), 403
    return jsonify({"message": "Invalid token please login first"}), 401


@assign_my_entries_routes.route('/api/v2/entries', methods=['GET'])
@cross_origin(origin='localhost:5000', headers=['Content-Type', 'Authorization'], supports_credentials=True)
def get_all_entries():
    """Uses a default user id to query the database and display all the entries
    associated with the user."""
    details = UserEntries()
    user_id = details.get_user_id()
    if isinstance(user_id, bool) is False:
        my_cursor.execute("""SELECT ID, TITLE, CONTENTS, DATEOFEVENT,
                          REMINDERTIME FROM ENTRIES WHERE USERID = %s 
                          ORDER BY ID;""", (user_id,))
        one_entry = my_cursor.fetchall()
        if one_entry:
            return jsonify({"message": one_entry, "user": user_id}), 200
        return jsonify({"message": "Your diary has no entries"}), 204
    return jsonify({"message": "Invalid token please login first"}), 401


@assign_my_entries_routes.route('/api/v2/entries/<int:entry_id>',
                                methods=['PUT'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def modify_entry(entry_id):
    """Used to modify diary entries."""
    details = UserEntries()
    user_id = details.get_user_id()
    if isinstance(user_id, bool) is False:
        if update_entry(entry_id, user_id, details.get_title(),
                        details.get_contents(), details.get_date_of_event(),
                        details.get_reminder_time()) is True:
            my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT,
                              REMINDERTIME FROM ENTRIES WHERE ID = %s AND
                              USERID = %s;""", (entry_id, user_id,))
            entry_in_database = my_cursor.fetchone()
            connection.commit()
            return jsonify({"message": entry_in_database}), 200
        return jsonify({"message": "entry not in database"}), 403
    return jsonify({"message": "Invalid token please login first"}), 401


@assign_my_entries_routes.route('/api/v2/entries/<int:entry_id>',
                                methods=['DELETE'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def delete_entry(entry_id):
    """Used to delete a diary entry"""
    try:
        payload = jwt.decode(request.args.get("user_token"),
                             "This is not the owner")
        user_id = payload['user']
    except jwt.exceptions.DecodeError:
        return jsonify({"message": "Invalid token please login first"})
    if remove_entry(entry_id, user_id) is True:
        return jsonify({"message": "Entry deleted from the database"}), 200
    return jsonify({"message": "entry not in the database"}), 403
