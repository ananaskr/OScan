import tldextract
from urllib.parse import urlparse,quote,unquote,parse_qs,parse_qsl

from library.URLExtract import urlextract
from library.sendrequests import request
from db.db import Database
from library.DiffResponse import diff
from db.logger import logger

db = Database()

class RedirectScan(object):

	def __init__(self,target):
		self.target = target
		self.repart = urlparse(self.target['url'])
		self.redirect = ''
		self.type = 'SOM Redirection'
		self.logger = logger()

	# Extract the redirect_uri value from the target url
	def fetch_redirect(self):
		query = parse_qs(self.repart.query)
		redirect = unquote(query['redirect_uri'][0])
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

	# Extract the Main Domain and fetch the same origin url.
	def extract_urls_from_homepage(self):
		rep = urlparse(self.redirect)
		val = tldextract.extract(self.redirect)
		domain = "{0}://{1}.{2}".format(rep.scheme,val.domain,val.suffix)
		target = {}
		target['url'] = domain
		res = request(target)
		urls = urlextract(self.redirect, res)
		return urls

	def check_cookie(self):
		if 'cookies' in self.target and self.target['cookies'] != '':
			return True
		else:
			return False

	# Combine the malformed redirect_uri parameter into
	def merge(self,muri):
		redirect_uri = quote(muri)
		query = parse_qs(self.repart.query)
		query['redirect_uri'] = redirect_uri.split(' ')

		new_query = ''
		for key,value in query.items():
			if new_query == '':
				new_query = new_query + key + '=' + value[0]
			else:
				new_query = new_query + '&' + key + '=' + value[0]
		return self.repart._replace(query=new_query).geturl()

	# Detection whether it is vulnerable.	
	def detect(self,muri,scanid):
		target = self.target
		target['url'] = muri
		res = request(target)
		if self.check_cookie():
			result = self.validate_code(res)
			if result:
				code = result
				return True
			else:
				return False
		else:
			result = self.validate_resp(res)
			if result:
				return True
			else:
				return False


def soredirect_scan(task):
	scan = RedirectScan(task['target1'])
	scan.fetch_redirect()
	uris = scan.extract_urls_from_homepage()
	for _ in uris:
		muri = scan.merge(_)
		result = scan.detect(_,task['scanid'])
		if result:
			print("%s[+]Target is vulnerable to SOM redirect attack. %s" % (scan.logger.Y,scan.logger.W))
			data = {"scanid":task['scanid'],"type":scan.type,"payload":muri}
			db.insert_record("Redirection",data)
			return True
