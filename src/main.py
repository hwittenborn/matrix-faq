#!/usr/bin/env -S -- python3 -u
import os
import requests
import json
import yaml
import time
import signal
from sqlalchemy import create_engine, MetaData, Table, Column, String, select

from functions.lint_config            import lint_config
from functions.make_request           import make_request
from functions.check_login_state      import check_login_state
from functions.batch_token            import get_batch_token, record_batch_token
from functions.join_rooms             import join_rooms
from functions.check_for_faq_messages import check_for_faq_messages
from functions.sig_handler            import sig_handler

# Make sure config file exists
if os.path.isfile("./config.yaml") == False:
	print("[Error] Couldn't find the configuration file.")
	print("[Error] Make sure 'config.yaml' exists in your current working directory.")
	quit(1)

# Make sure config file is readable
try:
	file = open("config.yaml", "r")
	yaml_data = file.read()
	file.close()
except PermissionError:
	print("[Error] Couldn't read the configuration file.")
	print("[Error] Make sure that you have at least read access to 'config.yaml', and try again.")

# Make sure config file has valid YAML syntax
try:
	yaml_formatted_data = yaml.load(yaml_data, Loader=yaml.SafeLoader)
except yaml.scanner.ScannerError:
	print("[Error] Your configuration file doesn't appear to have valid syntax.")
	quit(1)

# Make sure config file has all needed values
print("[Info] Linting config file...")
lint_config(yaml_formatted_data)

# Get needed values
username      = yaml_formatted_data["homeserver"]["username"]
password      = yaml_formatted_data["homeserver"]["password"]
homeserver    = yaml_formatted_data["homeserver"]["server"]

faq_prefix    = yaml_formatted_data["config"]["faq"]["prefix"]
faq_templates = yaml_formatted_data["config"]["faq"]["templates"]
faq_rooms     = yaml_formatted_data["config"]["rooms"]

# Set up database instance
try:
	engine = create_engine("sqlite:///./sqlite3.db", echo=False)
	conn = engine.connect()
except exc.OperationalError:
	print("[Error] Unable to open the database file.")
	print("[Error] Make sure that it is readable by your current user, and try again.")
	quit(1)

# Make sure database tables are set up
metadata = MetaData()

session_data = Table('session_data', metadata,
Column('name', String),
Column('value', String))

# Ensure tables exist
metadata.create_all(engine)

# Set up database table definition so we can pass them to functions
db_tables = {}
db_tables["session_data"] = session_data

# Create 'batch_token' row if if hasen't been added yet (only happens on first run).
sql_query = select([session_data]).where(session_data.c.name == "batch_token")
returned_sql_data = conn.execute(sql_query).fetchall()

if len(returned_sql_data) == 0:
	sql_query = session_data.insert().values(name="batch_token", value="")
	conn.execute(sql_query)

# Run prechecks
print("[Info] Running prechecks...")
print()

# Check login state
access_token = check_login_state(username, password, homeserver, conn, db_tables)

# Attempt to join all specified rooms
joined_rooms = join_rooms(access_token, homeserver, faq_rooms)

if len(joined_rooms) == 0:
	print("[Error] Unable to join all specified rooms.")
	quit(1)

# Purge current message queue (by getting a new batch token), as we might have a
# huge buildup of messages (which we don't want to process).
print("[Info] Purging message queue...")
batch_token = get_batch_token(conn, db_tables)

returned_data = make_request(username=username,
access_token=access_token,
homeserver=homeserver,
path=f"/sync")

record_batch_token(returned_data["next_batch"], conn, db_tables)

# Set up sigterm trap so we can exit gracefully
signal.signal(signal.SIGTERM, sig_handler)

# Go online
print("[Info] Going online.")

while True:

	# Obtain new messages
	batch_token = get_batch_token(conn, db_tables)

	returned_data = make_request(username=username,
	access_token=access_token,
	homeserver=homeserver,
	path=f"/sync?since={batch_token}")

	record_batch_token(returned_data["next_batch"], conn, db_tables)

	# Process returned data
	check_for_faq_messages(access_token, homeserver, returned_data, faq_prefix, faq_templates, joined_rooms)

	# Wait a bit so we don't slam the homeserver with requests
	time.sleep(0.1)
