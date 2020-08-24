import logging
import pyfiglet
from pyfiglet import Figlet
from clint.textui import puts, colored, indent
from logging import handlers

class logger(object):

	def __init__(self):
		self.G = '\033[0;32;40m'
		self.Y = '\033[0;33;40m'
		self.B = '\033[0;34;40m'
		self.R = '\033[0;31;40m'
		self.LB = '\033[0;36;40m'
		self.W = '\033[0m' 

	def banner(self):
		custom_fig = Figlet(font='Slant',justify="center")
		r = custom_fig.renderText('OScan')
		banner = colored.cyan(r)
		print(banner)
		print('%sAuthor: @ananskr%s'.center(80) % (self.LB,self.W))
		print('%sVersion: 1.0 beta%s'.center(80) % (self.LB,self.W))
		print('\n')
