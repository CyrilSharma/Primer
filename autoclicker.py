import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

class Autoclicker(threading.Thread):
	def __init__(self):
		super(Autoclicker, self).__init__()
		self.running = False
		self.program_running = True

	def start_clicking(self):
		self.running = True

	def stop_clicking(self):
		self.running = False

	def exit(self):
		self.stop_clicking()
		self.program_running = False