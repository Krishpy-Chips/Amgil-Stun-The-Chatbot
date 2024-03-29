if __name__ == "__main__":
	print("Start")

	import os
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"
	os.environ['DEBUG'] = "True"

	import json
	import pickle
	import requests

	from cloud.server import Server
	from local.data import Data
	from local.secerets import keys
	from model.ai import Ai

	try:
		requests.get("https://google.com")
		if len(keys["mongo_db"]) == 0:
			raise requests.exceptions.ConnectionError()
	except requests.exceptions.ConnectionError:
		Data.internet = False
	
	if Data.internet:
		server = Server()
		print("Logging in")

		with open("local/user_settings.json", "r") as user_settings_file:
			user_settings = json.load(user_settings_file)
		
		if user_settings["remember"]:
			try:
				with open("local/user_info.bin", "rb") as user_info_file:
					user_info = pickle.load(user_info_file)

				cloud_user = server.get_user(user_info["username"])

				if cloud_user["password"] == user_info["password"]:
					Data.login_allow = True
					Data.username = user_info["username"]
					Data.password = user_info["password"]
					print("Logged in")

			except FileNotFoundError:
				pass

	from gui.gui_exec.gui_main import Stun_Amgil	# Needs to be placed here for the autologin system to work
	from kivy.core.window import Window
	from kivy.utils import platform
	from kivy import require

	require("2.2.1")

	if platform == "android" or platform == "ios":
		Data.device = "phone"
		Window.maximize()
	else:
		Window.size = (1100, 600)
		Data.device = "pc"

	Stun_Amgil().run()