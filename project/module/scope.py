from urllib.parse import urlparse,quote,unquote,parse_qs

from config.config import get_file
from library.sendrequests import request
from library.DiffResponse import diff
from db.db import Database
from db.logger import logger

db = Database()
# Fuzzing the scope to detect if scope privilege escalation exists.
class ScopeScan:

	def __init__(self,target):
		self.scope = get_file('scope.txt')
		self.target = target
		self.redirect = ''
		self.type = 'Scope Escalation'
		self.logger = logger()

	def fetch_redirect(self):
		url = self.target['url']
		reparts = urlparse(url)
		query = parse_qs(reparts.query)
		redirect = query['redirect_uri']
		self.redirect = redirect[0]
		return redirect

	def mutate(self,scope):
		repart = urlparse(self.target['url'])
		query = parse_qs(repart.query)
		query['scope'] = scope.split(' ')

		new_query = ''
		for key,value in query.items():
			#print(value)
			if key == 'redirect_uri':
				value[0] = quote(value[0])
			if new_query == '':
				new_query = new_query + key + '=' + value[0]
			else:
				new_query = new_query + '&' + key + '=' + value[0]
		return repart._replace(query=new_query).geturl()
		


	def run(self):
		for _ in self.scope:
			muri= self.mutate(_)
			#muri = self.merge(mredirect)
			target = self.target
			target['url'] = muri
			res1 = request(self.target)
			res2 = request(self.target)
			res3 = request(target)
			result = diff(res1,res2,res3)
			return muri,result


def scope_scan(task):
	ss = ScopeScan(task.target1)
	ss.fetch_redirect()
	muri,result = ss.run()
	if not result:
		print("%s[+]Target is vulnerable to scope escalation attack. %s" % (ss.logger.G,ss.logger.W))
		data = {"scanid":task.scanid,"type":ss.type,"payload":muri}
		db.insert_record("Scope",data)
	return True



