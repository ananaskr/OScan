import hashlib
import time
from prettytable import PrettyTable
from module.csrfScan import csrf_scan
from module.scopeScan import scope_scan
from module.openRedirect import opredirect_scan
from module.covertRedirect import coredirect_scan
from module.soRedirect import soredirect_scan
from db.db import Database
from db.logger import logger

import copy

logger = logger()
db = Database()


'''
def show_result(task):
	self.db.fetch_records('csrf','{"scanid":"%s"}' % (self.scanid))


def code_valid(task):
	if 'cookies' in self.target1 and self.target1['cookies'] != '':
		code_scan(task)
	else:
		print('[-] Code Scan need to provide cookies or just provide An Authoration Code with -code.')


def token_valid(task):
	if 'cookies' in self.target1 and self.target1['cookies'] != '':
		token_scan(task)
	else:
		print('[-] Token Scan need to provide cookies or just provide An Authoration Code with -code.')
'''

def fetch_data(col,data,table,i):
	#print(data)
	result = db.fetch_records(col,data)
	for res in result:
		i += 1
		table.add_row([logger.G+str(i)+logger.W,logger.G+res['type']+logger.W,logger.G+res['payload']+logger.W])
	return table,i


		


def show_result(scanid):
	data = '{"scanid":"%s"}' % str(scanid)
	col = ['csrf','Scope','Redirection']
	table = PrettyTable(['id','vul type','payload'])
	i = 0
	for _ in col:
		table,i = fetch_data(_,data,table,i)
		#print("%s##############################################################%s" % (logger.G,logger.W))
		#print("\n")
	print(table)

		

def coRedirect(task):
	print("[ ]Covert Redirection Scan starting.")
	res = coredirect_scan(task)
	if res:
		print("[ ]Covert Redirection Scan has been completed.")


def soRedirect(task):
	print("[ ] Same Origin Redirection Scan starting.")
	res = soredirect_scan(task)
	if res:
		print("[ ]Same Origin Redirection Scan has been completed.")

def openRedirect(task):
	print("[ ]Open Redirction Scan starting.")
	res = opredirect_scan(task)
	if res:
		print("[ ]Open Redirection Scan has been completed.")

def scopeScan(task):
	print("[ ]Scope Escalation Scan starting.")
	res = scope_scan(task)
	if res:
		print("[ ]Scope Escalation Scan has been completed.")

def csrfScan(task):
	print("[ ]CSRF Scan starting.")
	res = csrf_scan(task)
	if res:
		print("[ ]CSRF Scan has been completed.")

def generate_scanid():
	scanid = hashlib.md5(str(time.time()).encode("utf-8")).hexdigest()
	return scanid

def scantask(target1,target2):
	scanid = generate_scanid()
	task = {}
	task['scanid'] = scanid
	task['target1'] = target1
	task['target2'] = target2
	task1 = copy.deepcopy(task)
	task2 = copy.deepcopy(task)
	task3 = copy.deepcopy(task)
	task4 = copy.deepcopy(task)
	# Start Scanning.
	# Start CSRF Scanning.
	csrfScan(task)
	# Start Scope Scanning.
	scopeScan(task1)
	# Start Redirection Scanning.
	# Start Open Redirection Scanning.
	openRedirect(task2)
	# Start Same Origin Redirection Scanning.
	soRedirect(task3)
	# Start Covert Redirection Scanning.
	# coRedirect(task4)
	# Start Authorization Code Verification
	print("[ ]Scan has been completed. Show the result.")
	show_result(scanid)
	





