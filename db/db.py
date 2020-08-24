from pymongo import MongoClient
import os
import json

class Database:
	def __init__(self):
		mongo_host = 'localhost'
		mongo_port = 27017

		self.client = MongoClient(mongo_host,mongo_port)
		self.db = self.client.oscan

	def fetch_records(self,col,param):
		param = json.loads(param)
		records = self.db[col].find(param)
		#print(records)
		#result = {}
		if records:
			return records
		else:
			return False


	def insert_record(self,collection,data):
		try:
			self.db[collection].insert(data)
		except Exception as e:
			raise e

	def update_record(self,coollection,find,update):
		try:
			self.db[collection].update(find,update)
		except Exception as e:
			raise e

if __name__ == '__main__':
	database = Database()

	database.fetch_records("csrf",'{"scanid":"844265ae69514a01638a5e8c9fc56449"}')

