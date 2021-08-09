def check_login_state(username, password, homeserver, conn, db_tables):
	import os
	import json
	import sqlite3
	from sqlalchemy.sql import select

	from functions.make_request import make_request

	session_data = db_tables["session_data"]

	# Check if we need to get an access token from the homeserver.
	# First we'll check if we even have an access token recorded. If we do,
	# we'll check if it's currently valid.
	get_new_access_token = True
	previous_access_token_present = False

	sql_query = select([session_data]).where(session_data.c.name == "access_token")

	returned_sql_data = conn.execute(sql_query).fetchall()

	if len(returned_sql_data) == 0:
		db_access_token = ""
	else:
		print("[Info] Checking that recorded access token is still valid...")
		db_access_token = returned_sql_data[0][1]

	if len(db_access_token) != 0:
		previous_access_token_present = True

		returned_request_data = make_request(username=username,
											 access_token=db_access_token,
											 homeserver=homeserver,
											 path="/account/whoami",
											 http_method="GET",
											 exception_error=False)

		# Check if current access token was valid.
		# Configure not to get a new one if so.
		try:
			if returned_request_data["errcode"] == "M_UNKNOWN_TOKEN":
				print("[Info] Access token doesn't appear to be valid. Going to obtain a new one.")
				pass
		except KeyError:
			print("[Info] Access token is valid.")
			get_new_access_token = False
			access_token = db_access_token

	if get_new_access_token == True:
		print("[Info] Obtaining access token...")
		# Generate JSON data to log in with
		matrix_request = {}
		matrix_request["type"] = "m.login.password"
		matrix_request["identifier"] = {}
		matrix_request["identifier"]["type"] = "m.id.user"
		matrix_request["identifier"]["user"] = username
		matrix_request["password"] = password
		matrix_request["initial_device_display_name"] = "matrix-faq"

		# Get access token to log in with
		formatted_matrix_request = json.dumps(matrix_request)
		returned_request_data = make_request(username=username,
											 homeserver=homeserver,
											 path="/login",
											 body=formatted_matrix_request,
											 http_method="POST",
											 exception_error=False)

		# Abort if a bad password was supplied
		try:
			if returned_request_data["errcode"] == "M_FORBIDDEN":
				print("[Error]: Invalid password was supplied.")
				quit(1)
		except KeyError:
			pass

		# Store access token in database
		access_token = returned_request_data["access_token"]

	if previous_access_token_present == False:
		sql_query = session_data.insert().values(name='access_token', value=f'{access_token}')
	else:
		sql_query = session_data.update().values(value=f"{access_token}").where(session_data.c.name == "access_token")

	conn.execute(sql_query)

	return(access_token)
