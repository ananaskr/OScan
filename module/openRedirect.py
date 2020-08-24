from urllib.parse import urlparse,quote,unquote,parse_qs,parse_qsl

from library.URLMutator import url_mutate
from library.sendrequests import request
from db.db import Database
from library.DiffResponse import diff
from db.logger import logger

class RedirectScan(object):

	def __init__(self,target):
		self.target = target
		self.repart = urlparse(target['url'])
		self.redirect = ''
		self.type = 'Open Redirection'
		self.logger = logger()
		self.db = Database()

	# Extract the redirect_uri value from the target url
	def fetch_redirect(self):
		query = parse_qs(self.repart.query)
		redirect = query['redirect_uri'][0]
		self.redirect = redirect
		return redirect

	# If cookie is provided, according the code to validate result.
	def validate_code(self,res):
		for i in range(len(res.history)):
			if "code" in res.history[i].headers['Location']:
				return urlparse(res.history[i].headers['Location']).query

		return False

	# If cookie is not provided, according to the comparation of responses.
	def validate_resp(self,res):
		res1 = request(self.target)
		res2 = request(self.target)
		result = diff(res1,res2,res)
		if result:
			return False
		else:
			return True


	# Combine the malformed redirect_uri parameter into
	def merge(self,muri):
		redirect_uri = quote(muri)
		query = parse_qs(self.repart.query)
		query['redirect_uri'] = quote(redirect_uri).split(' ')

		new_query = ''
		for key,value in query.items():
			if new_query == '':
				new_query = new_query + key + '=' + value[0]
			else:
				new_query = new_query + '&' + key + '=' + value[0]
		return self.repart._replace(query=new_query).geturl()

	def check_cookie(self):
		if 'cookies' in self.target and self.target['cookies'] != '':
			return True
		else:
			return False

	def detect(self,muri,scanid):
		target = self.target
		target['url'] = muri
		res = request(target)
		if self.check_cookie():
			result = self.validate_code(res)
			if result:
				code = result
				print("%s[+]Target is vulnerable to open redirect attack. %s" % (self.logger.Y,self.logger.W))
				data = {"scanid":scanid,"type":self.type,"payload":muri}
				self.db.insert_record("Redirection",data)
				return True
			else:
				return False
		else:
			result = self.validate_resp(res)
			if result:
				print("%s[+]Target is vulnerable to open redirect attack. %s" % (self.logger.Y,self.logger.W))
				data = {"scanid":scanid,"type":self.type,"payload":muri}
				self.db.insert_record("Redirection",data)
				return True
			else:
				return False



# Main function of redirect scan
def opredirect_scan(task):
	scan = RedirectScan(task['target1'])
	scan.fetch_redirect()
	muris = url_mutate(scan.redirect)
	for _ in muris:
		muri = scan.merge(_)
		valid = scan.detect(muri,task['scanid'])
	#print(task.target1)
	return True
		
