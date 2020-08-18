import hashlib
import time
from module.csrf import csrf_scan
from module.scope import scope_scan
from module.openRedirect import opredirect_scan
from module.covertRedirect import coredirect_scan
from module.soRedirect import soredirect_scan
from db.db import Database

class Scantask(object):

	def __init__(self,target1,target2=None):
		self.scanid = ''
		self.target1 = target1
		self.target2 = target2
		self.db = Database()


	def generate_scanid(self):
		scanid = hashlib.md5(str(time.time()).encode("utf-8")).hexdigest()
		self.scanid = scanid
		return scanid

	def csrfScan(self):
		print("[ ]CSRF Scan starting.")
		res = csrf_scan(self)
		if res:
			print("[ ]CSRF Scan has been completed.")

	def scopeScan(self):
		print("[ ]Scope Escalation Scan starting.")
		res = scope_scan(self)
		if res:
			print("[ ]Scope Escalation Scan has been completed.")

	def redirectScan(self):
		print("[ ]Redirection Scan starting")

		res = opredirect_scan(self)
		res = coredirect_scan(self)

		res = soredirect_scan(task2)

	def start(self):
		self.csrfScan()
		self.scopeScan()
		self.redirectScan()
		self.complete_scan()


	def show_result(self):

		self.db.fetch_records('csrf','{"scanid":"%s"}' % (self.scanid))




	def complete_scan(self):
		print("[+]Scan has been completed")
		self.show_result()


