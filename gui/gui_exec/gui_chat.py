import keyboard

from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.list import OneLineListItem
from kivymd.utils import asynckivy
#from kivy.core.window import Window, Keyboard

from win32com.client import Dispatch

from cloud.server import Server
from local.data import Data
from model.ai import Ai

class ChatScreen(Screen):

	chat_data = []
	speak = Dispatch("SAPI.SpVoice").Speak

	def __init__(self, **kw):
		super().__init__(**kw)
		self.chatbot = Ai(Data.model_number, Data.model_epochs, Data.model_batch, Data.model_dataset)
		#self.chatbot = Ai(3, 700, 8, "model/intents.json")
		self.server = Server()
		self.last_message = ""
		keyboard.add_hotkey('ctrl+t', self.bot_speak)
	
	def bot_speak(self):
		self.speak(self.last_message)

	def on_enter(self):

		def history_handler():
			async def populate():
				print("Populating start")
				print(self.chat_data)
				while True:
					if Data.loaded:
						break
				
				await asynckivy.sleep(1)

				user = self.server.get_chat(Data.username)
				chat_history = user["chat_history"]

				for chat_id in chat_history:
					if chat_id not in self.chat_data:
						self.ids.chat_data.add_widget(
							OneLineListItem(
								text=chat_history[chat_id]
							)
						)
						self.chat_data.append(chat_id)
				
				print("Populating end")
				print(self.chat_data)
				
			asynckivy.start(populate())
		
		if Data.internet:
			history_handler()

		return super().on_enter()


	def send_chat(self):
		async def send_handle():
			async def user_chat_handle():
				if len(self.ids.text_data.text) == 0:
					return
				
				user_response = self.ids.text_data.text

				self.ids.text_data.text = ""

				self.ids.chat_data.add_widget(
					OneLineListItem(
						text=f"You: {user_response}"
					)
				)

				bot_response = self.chatbot.ask_model(user_response.lower().strip())
				self.last_message = bot_response
				
				self.ids.chat_data.add_widget(
					OneLineListItem(
						text=f"Amgil Stun: {bot_response}"
					)
				)

				if Data.internet:
					user_chat_id = self.server.update_chat(Data.username,f"You: {user_response}")[1]
					bot_chat_id = self.server.update_chat(Data.username, f"Amgil Stun: {bot_response}")[1]

					self.chat_data.extend([user_chat_id, bot_chat_id])
			
			asynckivy.start(user_chat_handle())
			
		asynckivy.start(send_handle())