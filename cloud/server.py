import random

from pymongo import MongoClient
from pymongo import errors

from typing import Tuple

from local.secerets import keys
from local.data import Data

#import dns
#dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
#dns.resolver.default_resolver.nameservers=["8.8.8.8"]

class Server:
	def __init__(self) -> None:
		try:
			client = MongoClient(keys["mongo_db"], connect=False)
			print("Connected to DB")

			database = client["ChatDB"]

			collections = database.list_collection_names()
			if "ChatHistory" not in collections:
				database.create_collection("ChatHistory")
			if "Users" not in collections:
				database.create_collection("Users")
			
			self.chat_history = database["ChatHistory"]
			self.user_data    = database["Users"]
			
		except:
			Data.internet = False
			pass #client = databse = user_data = chat_history = None

	
	def get_user(self, username:str) -> (dict | None):
		return self.user_data.find_one({"_id":username})

	def get_all_users(self) -> list:
		return [user["_id"] for user in self.user_data.find({})]
	
	def post_user(self, username:str, password:str) -> bool:
		try:
			self.user_data.insert_one({"_id":username, "password":password})
		except errors.DuplicateKeyError:
			return False
		try:
			self.chat_history.insert_one({"_id":username, "chat_history":{}})
		except errors.DuplicateKeyError:
			return False
		return True


	def get_chat(self, username:str) -> (dict | None):
		if username == "G0":
			return {"_id":"G0", "chat_history":{}}
		return self.chat_history.find_one({"_id":username})

	def update_chat(self, username:str, message:str) -> Tuple[bool, str]:
		chat_hist = self.get_chat(username=username)
		if chat_hist is None:
			return (False, "-1")
		
		chat_tag = str(random.randint(1, 999999))
		chat_tag = "0" * (6 -len(chat_tag)) + chat_tag

		chat_hist["chat_history"][chat_tag] = message
		self.chat_history.update_one({"_id":username}, {"$set":{"chat_history": chat_hist["chat_history"]}})
		return (True, chat_tag)