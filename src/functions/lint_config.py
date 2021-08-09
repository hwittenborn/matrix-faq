def lint_config(yaml_formatted_data):
	# Process top-level items
	for i in ["homeserver", "config"]:
		try:
			if type(yaml_formatted_data[i]) != dict:
				print(f"[Error] Key '{i}' needs to be a dictionary.")
				quit(1)
		except KeyError:
			print(f"[Error] Key '{i}' is missing in config file.")

	# Process items under 'homeserver'
	for i in ['username', 'password', 'server']:
		try:
			if type(yaml_formatted_data["homeserver"][i]) != str:
				print(f"[Error] Key 'homeserver/{i}' needs to be a string.")
				quit(1)
		except KeyError:
			print(f"[Error] Key 'homeserver/{i}' is missing in configuration file.")
			quit(1)

	# Process 'config/rooms'
	try:
		if type(yaml_formatted_data["config"]["rooms"]) != list:
			print("[Error] Key 'config/rooms' needs to be a list.")
			quit(1)
	except KeyError:
		print("[Error] Key 'config/rooms' is missing in configuration file.")
		quit()

	# Process 'config/faq'
	try:
		if type(yaml_formatted_data["config"]["faq"]) != dict:
			print("[Error] Key 'config/faq' needs to be a dictionary.")
			quit(1)
	except KeyError:
		print("[Error] Key 'config/faq' is missing in configuration file.")
		quit(1)

	# Process 'config/faq/prefix'
	try:
		if type(yaml_formatted_data["config"]["faq"]["prefix"]) != str:
			print("[Error] Key 'config/faq/prefix' needs to be a string.")
			quit(1)
	except KeyError:
		print("[Error] Key 'config/faq/prefix' is missing in configuration file.")
		quit(1)

	# Process 'config/faq/templates'
	try:
		if type(yaml_formatted_data["config"]["faq"]["templates"]) != list:
			print("[Error] Key 'config/faq/templates' needs to be a list.")
	except KeyError:
		print("[Error] Key 'config/faq/templates' needs to be a list.")

	# Process templates in 'config/faq/templates'
	number = 0

	for i in yaml_formatted_data["config"]["faq"]["templates"]:
		for j in ["name", "value"]:

			if type(yaml_formatted_data["config"]["faq"]["templates"][number][j]) != str:
				print(f"[Error] Key 'config/faq/templates({number})/{j}' needs to be a string.")

		number = number + 1
