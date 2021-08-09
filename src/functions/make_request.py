def make_request(**args):
	import requests
	import json

	# Exception classes
	class MissingArgument(Exception):
		pass
	class BadArguments(Exception):
		pass
	class InvalidHttpMethod(Exception):
		pass
	class JSONParseError(Exception):
		pass
	class RequestError(Exception):
		pass

	# Process arguments
	username        = args.get("username")
	access_token    = args.get("access_token")
	homeserver      = args.get("homeserver")
	path            = args.get("path")
	body            = args.get("body")
	http_method     = args.get("http_method")
	client_endpoint = args.get("client_endpoint")
	exception_error = args.get("exception_error")

	# Make sure these are set.
	for i in [["homeserver", homeserver], ["path", path]]:
		if i[1] == None:
			raise MissingArgument(i[0])

	# We want to default to using the client endpoint when 'client_endpoint' is not set.
	if client_endpoint == True or client_endpoint == None:
		client_suffix = "/_matrix/client/r0"
	else:
		client_suffix = ""

	# We also want to default to using GET requests when there isn't one specified.
	if http_method == None:
		http_method = "GET"

	# We also want to default to throwing errors when requests return an error code
	if exception_error == None:
		exception_error = True

	# If a request method was specified though, make sure it's a supported type.
	if http_method != "GET" and http_method != "POST":
		raise InvalidHttpMethod(http_method)

	# Actually make the request.
	if http_method == "GET":
		if access_token == None:
			received_data = requests.get(f"{homeserver}{client_suffix}{path}", data = body)
		else:
			received_data = requests.get(f"{homeserver}{client_suffix}{path}", data = body, headers = {"Authorization": f"Bearer {access_token}"})

	elif http_method == "POST":
		if access_token == None:
			received_data = requests.post(f"{homeserver}{client_suffix}{path}", data = body)
		else:
			received_data = requests.post(f"{homeserver}{client_suffix}{path}", data = body, headers = {"Authorization": f"Bearer {access_token}"})

	# Validate returned data
	try:
		returned_data = json.loads(received_data.text)
	except json.decoder.JSONDecodeError:
		raise JSONParseError()

	try:
		errcode = returned_data["errcode"]
		error   = returned_data["error"]

		if exception_error == True:
			raise RequestError(errcode, error)
		else:
			return(returned_data)

	except KeyError:
		return(returned_data)
