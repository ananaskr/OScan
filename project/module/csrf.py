import re
import random
import string
from urllib.parse import urlparse,quote,unquote,parse_qs

from db.logger import logger

from config.config import get_file
from db.db import Database
from library.sendrequests import request
from library.DiffResponse import diff
from config.config import get_config

db = Database()


# CSRFScan detect the CSRF vulnerability in five scenes.
# [SAME TOKEN, TOKEN NOT VERIFY, NO TOKEN, DOUBLE TOKEN, WEAK TOKEN]
class CSRFScan:

	def __init__(self,target1,target2):
		self.logger = logger()
		self.target1 = target1
		self.target2 = target2
		self.csrf_query = get_config('csrf.property','query','csrf_name')
		self.csrf_header = get_config('csrf.property','headers','csrf_name')
		self.csrf_body = get_config('csrf.property','body','csrf_name')

	def same_token_detect(self,token1,token2):
		same = 0
		if token1.has_key('query'):
			if cmp(token1['query'],token2['query']) == 0:
				same = 1
			else:
				same = 0
		if token1.has_key('headers'):
			if cmp(token1['headers'],token2['headers']) == 0:
				same = 1 & same
			else:
				same = 0
		if token1.has_key('body'):
			if cmp(token1['body'],token2['body']) == 0:
				same = 1 & same
			else:
				same = 0

		return same

	def no_token_detect(self,target):
		csrf = {}
		repart = urlparse(target['url'])
		query = parse_qs(repart.query)
		for key,value in query.items():
			if key in self.csrf_query:
				data = {}
				data[key] = unquote(value[0])
				csrf['query'] = data

		headers = target['headers']
		for key,value in headers.items():
			if key in self.csrf_header:
				data = {}
				data[key] = unquote(value)
				csrf['headers'] = data

		body = target['body']
		if body != "":
			for key,value in body.items():
				if key in self.csrf_body:
					data = {}
					data[key] = unquote(value)
					csrf['body'] = key

		if len(csrf) == 0:
			return False
		else:
			return csrf


	def no_verify_detect(self,token):
		# CSRF token in query.
		if 'query' in token:
		#if token.has_key('query'):
			repart = urlparse(self.target1['url'])
			#print(repart)
			query = parse_qs(repart.query)
			for key,value in token['query'].items():
				#print(self.mutation_csrf_value(value))
				query[key] = self.mutation_csrf_value(value).split(' ')


			#print(query)
			new_query = ''
			for key,value in query.items():
				if key == 'redirect_uri':
					value[0] = quote(value[0])
				if new_query == '':
					new_query = new_query + key + '=' + value[0]
				else:
					new_query = new_query + '&' + key + '=' + value[0]
			#print(new_query)
			new_url = repart._replace(query=new_query).geturl()
			#print(new_url)

			target = self.target1
			target['url'] = new_url
		# CSRF token in headers 
		if 'headers' in token:
		#if token.has_key('headers'):
			header = self.target1['headers']
			for key,value in header.items():
			#key = token['headers'].keys()[0]
			#value = token['headers'][key]
				header[key] = self.mutation_csrf_value(value)

			target = self.target1
			target['headers'] = header
		# CSRF token in body.
		if 'body' in token:
		#if token.has_key('body'):
			body = self.target['body']
			for key,value in body.items():
			#key = token['body'].keys()[0]
			#value = token['body'][key]
				body[key] = self.mutation_csrf_value(value)

			target = self.target1
			target['body'] = body

		res1 = request(self.target1)
		res2 = request(self.target1)
		res3 = request(target)
		# Judge whether it is vulnerable.
		result = diff(res2,res3,res1)
		if not result:
			return True
		return False



	def double_token_detect(self,token):
		double = 0
		if 'query' in token and 'headers' in token:
		#if token.has_key('query') and token.has_key('headers'):
			query = token['query']
			header = token['headers']
			for key,value in query.items():
				for key1,value1 in header.items():
					if query.get(key) == header.get(key1):
						double = 1
		if 'query' in token and 'body' in token:
		#if token.has_key('query') and token.has_key('body'):
			query = token['query']
			body = token['body']
			for key,value in query.items():
				for key1,value1 in body.items():
					if query.get(key) == body.get(key1):
						double = 1 & double
		if 'headers' in token and 'body' in token:
		#if token.has_key('headers') and token.has_key('body'):
			header = token['headers']
			body = token['body']
			for key,value in header.items():
				for key1,value1 in body.items():
					if header.get(key) == body.get(key1):
						double = 1 & double

		return double


	def weak_token_detect(self,token):
		weak = 0
		if 'query' in token:
		#if token.has_key('query'):
			query = token['query']
			for key,value in query.items():
				if len(query.get(key)) <= 6:
					weak = 1
				else:
					weak = 0
		if 'headers' in token:
		#if token.has_key('headers'):
			header = token['headers']
			for key,value in header.items():
				if len(header.get(key)) <= 6:
					weak = 1 & weak
				else:
					weak = 0 
		if 'body' in token:
		#if token.has_key('body'):
			body = token['body']
			for key,value in body.items():
				if len(body.get(key)) <= 6:
					weak = 1 & weak
				else:
					weak = 0

		return weak

	def remove_token_detect(self,token):
		if 'query' in token:
		#if token.has_key('query'):
			repart = urlparse(self.target1['url'])
			query = parse_qs(repart.query)
			key = ''
			for key1,value1 in token['query'].items():
				key = key1

			del query[key]
			new_query = ''
			for key,value in query.items():
				if key == 'redirect_uri':
					value[0] = quote(value[0])
				if new_query == '':
					new_query = new_query + key + '=' + value[0]
				else:
					new_query = new_query + '&' + key + '=' + value[0]
			new_url = repart._replace(query=new_query).geturl()

			target = self.target1
			target['url'] = new_url
		if 'headers' in token:
		#if token.has_key('headers'):
			header = self.target1['headers']
			for key1,value1 in token['headers'].items():
				key = key1
			del header[key]

			target = self.target1
			target['headers'] = header
		# CSRF token in body.
		if 'body' in token:
		#if token.has_key('body'):
			body = self.target1['body']
			for key1,value1 in token['body'].items():
				key = key1
			del body[key]

			target = self.target1
			target['body'] = body

		res1 = request(self.target1)
		res2 = request(self.target1)
		res3 = request(target)
		# Judge whether it is vulnerable.
		result = diff(res1,res2,res3)
		if not result:
			return True
		return False


	def mutation_csrf_value(self,content):
		length = len(content)
		new_csrf_token = ''.join(random.choice(string.ascii_letters) for i in range(length))
		return new_csrf_token


def csrf_scan(task):
	if 'headers' not in task.target1:
	#if not task.target1.has_key('headers'):
		print("Please input the complete information to detect csrf.")
		exit()
	if not task.target2:
		print("If want more accurate result, another one request should be provided with -r options")
	csrf = CSRFScan(task.target1,task.target2)
	# No csrf token detected.
	token = csrf.no_token_detect(task.target1)
	#print('qkl')
	if not token:
		print("%s[+]Target is vulnerable to csrf attack%s" % (csrf.logger.G,csrf.logger.W))
		data = {"scanid":task.scanid,"url":csrf.target1['url'],"type":"csrf attack","payload":"no csrf token provide"}
		db.insert_record('csrf',data)
		exit()
	# Weak csrf token detected.
	weak = csrf.weak_token_detect(token)
	if weak:
		print("%s[+]Target is vulnerable to csrf attack%s" % (csrf.logger.G,csrf.logger.W))
		data = {"scanid":task.scanid,"url":csrf.target1['url'],"type":"csrf attack","payload":"weak csrf token provide"}
		db.insert_record('csrf',data)
	# Same csrf token detected, ie use same value in every request.
	if task.target2:
		token1 = csrf.no_token_detect(task.target2)
		same = csrf.same_token_detect(token,token1)
		if same:
			print("%s[+]Target is vulnerable to csrf attack%s" % (csrf.logger.G,csrf.logger.W))
			data = {"scanid":task.scanid,"url":csrf.target1['url'],"type":"csrf attack","payload":"same csrf token provide"}
			db.insert_record('csrf',data)
	# Double csrf token detected.
	double = csrf.double_token_detect(token)
	if double:
		print("%s[+]Target is vulnerable to csrf attack%s" % (csrf.logger.G,csrf.logger.W))
		data = {"scanid":task.scanid,"url":csrf.target1['url'],"type":"csrf attack","payload":"double csrf token provide"}
		db.insert_record('csrf',data)
	# Server verify csrf token or not.
	verify = csrf.no_verify_detect(token)
	if verify:
		print("%s[+]Target is vulnerable to csrf attack%s" % (csrf.logger.G,csrf.logger.W))
		data = {"scanid":task.scanid,"url":csrf.target1['url'],"type":"csrf attack","payload":"miss csrf token verify"}
		db.insert_record('csrf',data)
	# Remove 
	remove = csrf.remove_token_detect(token)
	if remove:
		print("%s[+]Target is vulnerable to csrf attack%s" % (csrf.logger.G,csrf.logger.W))
		data = {"scanid":task.scanid,"url":csrf.target1['url'],"type":"csrf attack","payload":"remove csrf token succeed"}
		db.insert_record('csrf',data)
	return True