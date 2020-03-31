import os
import sys
import json
import time
import hashlib
import argparse
import webbrowser
import requests

from modules.oauth_scan import oauth_scan
from utils.logger import logger
from utils.db import Database

def scan_complete():
	print("[+]Scan has been completed")
	webbrowser.open("http://127.0.0.1/reports.html#"+scanid)
	while True:
		pass


def check_network():
	try:
		res = requests.get("http://www.baidu.com")
		return True
	except Exception as e:
		print("[-]%s Failed to connect the network%s"%(scan_logger.R,scan_logger.W))
		return False


def check_database():
	try:
		db = Database()
		data = {}
		db.insert_record("result",data)
		return True
	except Exception as e:
		print("[-]%s Database connection refuse%s"%(scan_logger.R,scan_logger.W))
		return False


def generate_scanid():
	scanid = hashlib.md5(str(time.time()).encode("utf-8")).hexdigest()
	return scanid

def get_arg(args=None):
	parser = argparse.ArgumentParser(description='OScan - OAuth Web Security testing Framework')
	parser.add_argument('-req1','--api_requests_1',help='')
	parser.add_argument('-req2','--api_requests_2',help='')
	parser.add_argument('--f','--filename',help='',default='')

	results = parser.parse_args(args)
	if len(args) == 0:
		print("At least one argument is needed to procced.\nFor further information check help: python astra.py --help")
		sys.exit(1)

	request_1 = json.loads(results.api_requests_1)
	url1 = request_1['url']
	method = request_1['method']
	headers1 = request_1['headers']
	body1 = request_1['body']

	request_2 = json.loads(results.api_requests_2)
	url2 = request_2['url']
	headers2 = request_1['headers']
	body2 = request_1['body']

	return url1,method,headers1,body1,url2,headers2,body2


def main():
	url1,method,headers1,body1,url2,headers2,body2 = get_arg(sys.argv[1:])
	scanid = generate_scanid()
	print("starting scanning........")
	oauth_scan(scanid,url1,method,headers1,body1,url2,headers2,body2)
	print("complete scanning........")



if __name__ == '__main__':
	scan_logger = logger()
	scan_logger.banner()
	if check_database() and check_network():
		main()
	else:
		print("exit.")