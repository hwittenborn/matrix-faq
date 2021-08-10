def join_rooms(access_token, homeserver, faq_rooms):
	import json
	from functions.make_request import make_request

	joined_rooms = []

	print()
	print("[Info] Attempting to join specified rooms...")
	print()

	for i in faq_rooms:
		# Format room name
		room_name = i.replace(":", "%3A").replace("#", "%23")

		# Attempt to join the room
		returned_data = make_request(access_token = access_token,
									 homeserver = homeserver,
									 path = f"/join/{room_name}",
									 http_method = "POST",
									 exception_error = False)

		try:
			if returned_data["errcode"] == "M_UNKNOWN":
				print(f"[Warning-M_UNKNOWN]: Unable to find room '{i}'.")
			elif returned_data["errcode"] == "M_FORBIDDEN":
				print(f"[Warning-M_FORBIDDEN]: Unable to join room '{i}'.")

		except KeyError:
			joined_rooms += [returned_data["room_id"]]

	# Quit if we were unable to join all rooms.
	if len(joined_rooms) == 0:
		print()
		print("[Error] Unable to join all specified rooms.")
		quit(1)

	else:
		if len(faq_rooms) != len(joined_rooms):
			print()
			print("[Warning] Couldn't join all specified rooms.")
		else:
			print("[Info] Succesfully joined all specified rooms.")

		print()
		return joined_rooms
