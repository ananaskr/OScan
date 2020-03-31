from pymongo import MongoClient
import os
import json

class Database:
	def __init__(self):
		mongo_host = 'localhost'
		mongo_port = 27017

		self.client = MongoClient(mongo_host,mongo_port)
		self.db = self.client.oscan

	def fetch_records(self,param):
		param = json.loads(param)[0]
		print(param)
		records = self.db.result.find(param)
		if records:
			for data in records:
				data.pop('_id')
				print(data)

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

#if __name__ == '__main__':
#	database = Database()
	#param = """[{"scanid":12}]"""
	#database.fetch_records(param)
#	data = {"url":"http://test.com","description":"state same","payload":"http://test.com?state={}"}
#	database.insert_record("csrf_result",data)

