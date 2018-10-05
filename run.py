from flask import Flask, request, jsonify
import json, datetime, os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = "TheOwner"
my_database = {}

@app.route('/', methods=['GET', 'POST'])
def home():
	return jsonify({"message": "Welcome to my home page"})


@app.route('/register', methods=['POST'])
def register():
	"""Loads the contents of the file, retrieves information
	sent by the requests, checks for a unique email, and 
	inserts the infromation into my_databse before writing back
	inserts the information into my_databse before writing back
	modify-entry into the file."""
	details_from_post = request.get_json()
	firstname = details_from_post.get("firstname", None)
	lastname = details_from_post.get("lastname", None)
	email = details_from_post.get("email", None)
	password = details_from_post.get("password", None)
	password2 = details_from_post.get("password2", None)
	if email in my_database:
		return jsonify({"message": "Email Taken."})
	else:
		my_database[email] = user_details
		return jsonify({"Firstname":firstname, "lastname": lastname,
						"message": "Successfully registered." })

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Loads the database from a file, retrieves and validates the
	password and eamil with the one present in the databse, and
	generates an access toke for the user."""
	details_from_post = request.get_json()
	email = details_from_post.get("email", None)
	password = details_from_post.get("password", None)
	# email = 'sikolia21.wycliffe@gmail.com'
	# password = 'password'
	if email in my_database:
		if password == my_database.get(email, None)[2]:
			access_token = jwt.encode({'user':email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])
			return jsonify({'access_token': access_token.decode('utf-8'), 'message':'Log in successful'})
		else:
			return jsonify({"message":"Invalid credentials"})
	else:
		return jsonify({"message":"Invalid credentials"})


@app.route('/entries', methods=['POST'])
def add_entries():
	"""Loads datbase from the file, retrieves information
	from the request, and updates the information in the 
	database."""
	details_from_post = request.get_json()
	email = details_from_post.get("email", None)
	entry = details_from_post.get("entry", None)#recieved as a list
	user_details = my_database.get(email, None)
	append_entry_to = user_details[3]
	for entry in entry:
		append_entry_to.append(entry)
	user_details.append(append_entry_to)
	my_database[email] = user_details
	return jsonify({user_details[0]: "entry Added", 'entries': user_details[3]})

@app.route('/entries', methods=['GET'])
def get_entries():
	"""Fetches information from the databse, gets 
	all user entries from the database, uses an 
	email provided in the code to retrieve entries
	from the ddatabase."""
	email = "sikolia21.wycliffe@gmail.com"
	user_details = my_database.get(email, None)
	return jsonify({"email": email,
					"entries": user_details[3]})

@app.route('/entries/<int:entryId>', methods=['GET'])
def get_one_entry(entryId):
	"""Uses a default email to query my_database for the user details,
	retrieves user entries from the user details and uses an id sent
	from the request to fetch the entry in the user_entries. """
	email = "sikolia21.wycliffe@gmail.com"
	user_details = my_database.get(email, None)
	user_entries = user_details[3]
	requested_entry = user_entries[entryId]
	return jsonify({"email": email,
					"Requested_entry": requested_entry})

@app.route('/entries/<int:entryId>', methods=['PUT'])
def modify_entry(entryId):
	"""Uses a default email to query my_database for the user details,
	retrieves user entries from the user details and uses an id sent
	from the request to modify the entry in the user_entries."""
	details_from_post = request.get_json()
	entry = details_from_post.get("entry", None)
	email = details_from_post.get("email", None)
	user_details = my_database.get(email, None)
	user_entries = user_details[3]
	requested_entry = user_entries[entryId]
	user_entries[entryId] = entry
	return jsonify({"email": email,
					"Requested_entry": entry})


if __name__ == "__main__":
	app.run(debug = True, port=5000)
