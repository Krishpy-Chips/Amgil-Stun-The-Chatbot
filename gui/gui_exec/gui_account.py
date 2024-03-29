import os
from kivymd.uix.screen import Screen

from local.data import Data
from gui.gui_exec.gui_chat import ChatScreen

class AccountScreen(Screen):
	def __init__(self, **kw):
		self.username = Data.username
		self.password = "*" * len(Data.password)
		super().__init__(**kw)
	
	def on_enter(self):
		self.username = Data.username
		self.password = "*" * len(Data.password)
		#self.manager.get_screen("kv_account_screen").ids.

		return super().on_enter()
	
	def logout(self):
		ChatScreen.chat_data.clear()
		Data.password = "*****"
		Data.username = "G0"
		self.manager.get_screen("kv_chat_screen").ids.chat_data.clear_widgets()

		try:
			os.remove("local/user_info.bin")
		except FileNotFoundError:
			pass