import tldextract
from urllib.parse import urlparse,quote,unquote,parse_qs,parse_qsl

from library.URLExtract import urlextract
from library.sendrequests import request
from db.db import Database
from library.DiffResponse import diff
from db.logger import logger
from core.spider import spider
from core.openredirect import openredirect

db = Database()

class RedirectScan(object):

	def __init__(self,target):
		self.target = target
		self.repart = urlparse(self.target['url'])
		self.redirect = ''
		self.type = 'Covert Redirection'
		self.logger = logger()

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
		redirect_uri = quote(redirect_uri)
		query = parse_qs(self.repart.query)
		query['redirect_uri'] = redirect_uri

		new_query = ''
		for key,value in query.items():
			if new_query == '':
				new_query = new_query + key + '=' + value
			else:
				new_query = new_query + '&' + key + '=' + value
		return self.repart._replace(query=new_query).geturl()

	# Craw uris which support open redirect.
	def craw_uri(self,main):
		uris = spider(main)
		redire_uris = []
		for _ in uris:
			res = openredirect(_)
			if res:
				redire_uris.append(res)

		return redire_uris

	def fetch_main(self):
		val = tldextract.extract(self.redirect)
		rep = urlparse(self.redirect)
		domain = "{0}://{1}.{2}".format(rep.scheme,val.domain,val.suffix)
		print(domain)
		return domain

	def detect(self,scanid):
		main = self.fetch_main()
		res = self.craw_uri(main)
		if res:
			for _ in res:
				muri = self.merge(_)
				result = request(muri)
				if self.check_cookie():
					result = self.validate_code(res)
					if result:
						code = result
						print("%s[+]Target is vulnerable to SOM redirect attack. " % (self.logger.G,self.logger.W))
						data = {"scanid":scanid,"type":self.type,"payload":muri}
						db.insert_record("Redirection",data)
						return True
					else:
						return False
				else:
					result = self.validate_resp(res)
					if result:
						print("%s[+]Target is vulnerable to SOM redirect attack. " % (self.logger.G,self.logger.W))
						data = {"scanid":scanid,"type":self.type,"payload":muri}
						db.insert_record("Redirection",data)
						return True
					else:
						return False
		return False


def coredirect_scan(task):
	scan = RedirectScan(task.target1)
	scan.fetch_redirect()
	scan.detect(task.scanid)



