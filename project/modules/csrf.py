import re

from utils.logger import logger
from urllib.parse import urlparse,quote,unquote,parse_qs
from utils.config import get_list
from utils.db import Database
from core.sendrequests import request_send
from core.diff import diff_text,diff_headers,diff_status_code

db = Database()
scan_logger = logger()

global scanid

def diff_analyze(res1,res2,res3):
	if diff_status_code(res1,res3):
		return True
	if diff_headers(res1,res2,res3):
		return True
	if diff_text(res1,res2,res3):
		return True

	return False

def mutation_csrf_value(content):
	# the various method
	csrf_collection = []
	csrf_collection.append("")
	for key,value in content.items():
		length = len(value)
		new_csrf_token = ''.join(random.choice(string.ascii_letters) for i in range(length))
		csrf_collection.append(new_csrf_token)

def csrf_attack_body(scanid,url,method,headers,body,csrf_body):
	new_data = []
	muta_token = mutation_csrf_value(csrf_body)

	#remove the csrf token
	keys,values = csrf_body.items()
	new_body = body
	new_body.pop(keys)
	
	req_origin1 = request_send(url,method,headers,body)
	req_origin2 = request_send(url,method,headers,body)
	req_mutation = request_send(url,method,headers,new_body)

	if diff_analyze(req_origin1,req_origin2,req_mutation):
		data = {"scanid":scanid,"url":url,"type":"csrf body","vul":"csrf check empty","payload":new_body}
		db.insert_record("csrf_reult",data)

	#replace the csrf token
	new_headers = headers
	for csrf_token in muta_token:
		new_headers[key] = csrf_token
		
		req_origin1 = request_send(url,method,headers,body)
		req_origin2 = request_send(url,method,headers,body)
		req_mutation = request_send(url,method,headers,new_body)

		if diff_analyze(req_origin1,req_origin2,req_mutation):
			data = {"scanid":scanid,"url":url,"type":"csrf body","vul":"csrf check lack","payload":new_body}
			db.insert_record("csrf_reult",data)
	

def csrf_attack_header(scanid,url,method,headers,csrf_header):
	new_data = []
	muta_token = mutation_csrf_value(csrf_header)

	# remove the csrf token
	new_headers = headers
	keys,values = csrf_header.items()
	new_headers.pop(keys)

	req_origin1 = request_send(url,method,headers,body)
	req_origin2 = request_send(url,method,headers,body)
	req_mutation = request_send(new_url,method,new_headers,body)

	if diff_analyze(req_origin1,req_origin2,req_mutation):
		data = {"scanid":scanid,"url":url,"type":"csrf headers","vul":"csrf check empty","payload":new_headers}
		db.insert_record("csrf_reult",data)




	# replace the csrf token
	new_headers = headers
	for csrf_token in muta_token:
		new_headers[key] = csrf_token
		
		req_origin1 = request_send(url,method,headers,body)
		req_origin2 = request_send(url,method,headers,body)
		req_mutation = request_send(new_url,method,new_headers,body)

		if diff_analyze(req_origin1,req_origin2,req_mutation):
			data = {"scanid":scanid,"url":url,"type":"csrf headers","vul":"csrf check lack","payload":new_headers}
			db.insert_record("csrf_reult",data)


def csrf_attack_url(scanid,url,method,headers,body,csrf_url):
	new_data = []
	muta_token = mutation_csrf_value(csrf_url)
	re_parts = urlparse(url)
	temp_query = parse_qs(re_parts.query)

	# remove csrf_token parameter
	keys,values = csrf_url.items()
	new_query = ''
	for key,value in temp_query:
		if key != keys:
			if len(new_query):
				new_query = new_query+'&'+key+'='+value
			else:
				new_query = key+'='+value

	new_url = re_parts._replace(query=new_query).geturl()

	req_origin1 = request_send(url,method,headers,body)
	req_origin2 = request_send(url,method,headers,body)
	req_mutation = request_send(new_url,method,headers,body)


	if diff_analyze(req_origin1,req_origin2,req_mutation):
			data = {"scanid":scanid,"url":url,"type":"csrf url","vul":"csrf check lack","payload":url1}
			db.insert_record("csrf_reult",data)

	# replace csrf_token parameter
	for csrf_token in muta_token:
		temp_query[csrf_url] = csrf_token
		new_query = ''
		for key,value in temp_query:
			if len(new_query):
				new_query = new_query+'&'+key+'='+value
			else:
				new_query = key+'='+value
		
		new_url = re_parts._replace(query=new_query).geturl()


		req_origin1 = request_send(url,method,headers,body)
		req_origin2 = request_send(url,method,headers,body)
		req_mutation = request_send(new_url,method,headers,body)

		if diff_analyze(req_origin1,req_origin2,req_mutation):
			data = {"scanid":scanid,"url":url,"type":"csrf url","vul":"csrf check lack","payload":url1}
			db.insert_record("csrf_reult",data)



def fetch_name(type):	
	return get_list("csrf.property",type,"csrf_name")


def fetch_url(url):
	#obtained the parameter
	res = {}
	csrf_name = fetch_name("url")
	param = parse_qs(urlparse(url).query)
	for name in csrf_name:
		for key,value in param.items():
			if key in name:
				res[key] = value
				return res

	return False


def fetch_header(headers):
	res = {}
	csrf_name = fetch_name("headers")
	for name in csrf_name:
		for key,value in headers.items():
			if key in name:
				res[key] = value
				return res

	return False


def fetch_body(body):
	res = {}
	csrf_name = fetch_name("body")
	for name in csrf_name:
		for key,value in body.items():
			if key in name:
				res[key] = value
				return res

	return False

def two_factor(first,second):
	(key1,value1), = first.items()
	(key2,value2), = second.items()
	if value1 == value2:
		return True
	else:
		return False


def csrf_scan(scanid,url1,method,headers1,body1,url2,headers2,body2):
	try:
		csrf_url_1 = fetch_url(url1)
		csrf_url_2 = fetch_url(url2)

		csrf_header_1 = fetch_header(headers1)
		csrf_header_2 = fetch_header(headers2)

		if csrf_url_1 and csrf_header_1:
			if two_factor(csrf_url_1,csrf_header_1):
				print("%s[+]{0} is vulnerable to csrf attack%s".format(scanid)%(scan_logger.G,scan_logger.W))
				data = {"scanid":scanid,"url":url1,"type":"two factor","vul":"only need the csrf token are same","payload":url1+" "+headers1}
				db.insert_record("csrf_reult",data)

		if csrf_url_1 and not csrf_header_1:
			print(csrf_url_1)
			(key1,value1), = csrf_url_1.items()
			(key2,value2), = csrf_url_2.items()
			if value1 == value2:
				print("%s[+]{0} is vulnerable to csrf attack%s".format(scanid)%(scan_logger.G,scan_logger.W))
				data = {"scanid":scanid,"url":url1,"type":"csrf token in url","vul":"csrf token is fixed","payload":url1}
				db.insert_record("csrf_result",data)
			else:
				csrf_attack_url(scanid,url1,method,headers1,csrf_url_1)

		if csrf_header_1 and not csrf_url_1:
			(key1,value1), = csrf_header_1.items()
			(key2,value2), = csrf_header_2.items()
			if value1 == value2:
				print("%s[+]{0} is vulnerable to csrf attack%s".format(scanid)%(scan_logger.G,scan_logger.W))
				data = {"scanid":scanid,"url":url1,"type":"csrf token in headers","vul":"csrf token is fixed","payload":headers1}
				db.insert_record("csrf_result",data)
			else:
				csrf_attack_header(scanid,url1,method,headers1,csrf_header_1)

		if method == "POST":
			print(body1)
			csrf_body_1 = fetch_body(body1)
			csrf_body_2 = fetch_body(body2)

			if csrf_body_1 and not csrf_header_1 and not csrf_url_1:
				(key1,value1), = csrf_body_1.items()
				(key2,value2), = csrf_body_2.items()
				if value1 == value2:
					print("%s[+]{0} is vulnerable to csrf attack%s".format(scanid)% (scan_logger.G,scan_logger.W))
					data = {"scanid":scanid,"url":url1,"type":"csrf token in bodys","vul":"csrf token is fixed","payload":body1}
					db.insert_record("csrf_result",data)
				else:
					csrf_attack_body(scanid,url1,method,headers1,csrf_body_1)

			if csrf_body_1 and csrf_header_1 and not csrf_url_1:
				if two_factor(csrf_body_1,csrf_header_1):
					print("%s[+]{0} is vulnerable to csrf attack%s".format(scanid)%(scan_logger.G,scan_logger.W))
					data = {"scanid":scanid,"url":url1,"type":"two factor","vul":"only need the csrf token are same","payload":url1+" "+body1}
					db.insert_record("csrf_reult",data)

			if csrf_body_1 and csrf_url_1 and not csrf_header_1:
				if two_factor(csrf_body_1,csrf_url_1):
					print("%s[+]{0} is vulnerable to csrf attack%s".format(scanid)%(scan_logger.G,scan_logger.W))
					data = {"scanid":scanid,"url":url1,"type":"two factor","vul":"only need the csrf token are same","payload":url1+" "+body1}
					db.insert_record("csrf_reult",data)

	except Exception as e:
		raise e