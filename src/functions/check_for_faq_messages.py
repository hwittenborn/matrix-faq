def check_for_faq_messages(access_token, homeserver, returned_data, faq_prefix, faq_templates, joined_rooms):
	import json
	import re
	import markdown

	from functions.make_request import make_request

	try:
		rooms_with_new_messages = list(returned_data["rooms"]["join"])

		for i in rooms_with_new_messages:
			# Abort if room isn't a room specified in config file
			valid_room = False

			for j in joined_rooms:
				if i == j:
					valid_room = True

			if valid_room == False:
				print(f"[Warning] Skipping message from '{i}', as room wasn't specified in configuration file.")
				continue

			room_events = returned_data["rooms"]["join"][i]["timeline"]["events"]

			room_id = i.replace(':', '%3A')

			for i in room_events:
				if i["content"]["msgtype"] == "m.text":
					# Squeeze spaces
					message = i["content"]["body"]
					message = re.sub(" +", " ", message)

					# Check if message has FAQ prefix
					if re.search(f"^{faq_prefix}", message) != None:
						message_no_prefix = re.sub(f"^{faq_prefix}", "", message)

						matrix_request = {}
						matrix_request["msgtype"] = "m.text"
						matrix_request["format"] = "org.matrix.custom.html"

						if message_no_prefix == "" or message_no_prefix == " ":
							matrix_request["body"]           = "Available templates:\n"
							matrix_request["formatted_body"] = markdown.markdown(matrix_request["body"])

							for i in faq_templates:
								template_value = i["name"]
								matrix_request["body"]           += f"- {template_value}\n"
								matrix_request["formatted_body"] += markdown.markdown(f"- {template_value}\n")

						# Abort if the resulting message doesn't start with a
						# space, as that means something like '{faq_prefix}template'
						# was passed instead of '{faq_prefix} template'.
						else:
							if re.match("^ ", message_no_prefix) == None:
								return
							else:
								message_no_prefix = re.sub("^ ", "", message_no_prefix)

							# We'll override this if a template is found.
							# We use it to show an error message to the user
							# if a template is not found.
							template_found = False

							for i in faq_templates:

								# Template was found, so we generate the template
								# based on it's value.
								if message_no_prefix == i["name"]:
									template_found = True
									matrix_request["body"] = i["value"]
									matrix_request["formatted_body"] = markdown.markdown(i["value"])
									break

							# Template was not found, so we bring up the error screen.
							if template_found == False:

								matrix_request["body"]            = "Couldn't find the requested FAQ template.\n"
								matrix_request["body"]           += f"Available FAQ templates can be found with `{faq_prefix}`."
								matrix_request["formatted_body"]  = markdown.markdown(matrix_request["body"])

						# Finally: send the actual request.
						make_request(access_token=access_token,
									 homeserver=homeserver,
									 path=f"/rooms/{room_id}/send/m.room.message",
									 body=json.dumps(matrix_request),
									 http_method="POST")

	except KeyError:
		pass
