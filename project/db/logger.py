import logging
from logging import handlers

class logger(object):

	def __init__(self):
		self.G = '\033[0;32;40m'
		self.Y = '\033[0;33;40m'
		self.B = '\033[0;34;40m'
		self.R = '\033[0;31;40m'
		self.W = '\033[0m' 


	def banner(self):
		print('''%s			
		   _____
		  / _,_ \\
		 / /   \\ \\   ___    ___    __ _   _____ 
		| |     | | / __   / _ \  / _  | |  _  |
		 \ \___/ /  \__ \ | (_   | (_| | | | | |
		  \_____/   \___/  \___/  \__,_| | | | |
			%s'''%(self.G,self.W))
