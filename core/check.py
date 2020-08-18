import requests
from db.db import Database

from db.logger import logger


# This class include the initiate check to start scan.
# [NETWORK, DATABASE]
class Check(object):

	def __init__(self):
		self.logger = logger()

	# Check connectivity of network. 
	def check_network_out(self):
		try:
			res = requests.get("http://www.baidu.com")
			return True
		except Exception as e:
			return False

	# Check connectivity of database.
	def check_database(self):
		try:
			db = Database()
			data = {}
			db.insert_record("result",data)
			return True
		except Exception as e:
			print("[-]%s Database connection refuse%s"%(logger.R,logger.W))
			return False
	
	# Check connectivity of network. 
	def check_network_in(self):
		print("It seems that you can not establish a connection with the external network.")
		options = input("If you are in Intranet: (input y:n)")
		if options == 'y':
			return True
		else:
			print("[-]%s Failed to connect the network%s"%(logger.R,logger.W))
			return False


def check():
	check = Check()
	res = check.check_network_out()
	if not res:
		if not check.check_network_in():
			print("Exit.")
			exit()
	if check.check_database():
		return True
	else:
		return False
