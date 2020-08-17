from urllib.parse import urlparse,quote,unquote,parse_qs,parse_qsl

from config.config import get_file
from library.sendrequests import request


class OpenRedirection(object):

	def __init__(self,target):
		self.target = target
		self.key = ''
		self.redirect = get_file('redirect_payload.txt')

	# Check whether redirect param in this uri.
	def check_redirect(self):
		names = get_file('redirect.txt')
		reparts = urlparse(self.target)
		query = parse_qs(reparts.query)
		for key,value in query.items():
			if key in names:
				self.key = key
				return True
		return False

	# Merge the payload with uri.
	def merge(self,uri):
		reparts = urlparse(self.target)
		query = parse_qs(reparts.query)
		query[self.key] = quote(uri)
		
		new_query = ''
		for key,value in query.items():
			if new_query == '':
				new_query = new_query + key + '=' + value
			else:
				new_query = new_query + '&' + key + '=' + value
		return self.reparts._replace(query=new_query).geturl()



	def scan(self):
		if check_redirect():
			for _ in self.redirect:
				uri = merge(_)
				res = request(uri)
				if res.status_code[0] == '3':
					if res.headers['Location'].startswith(_) is True:
						return uri
		else:
			# Add 
			self.target = self.target + "?url="
			for _ in self.redirect:
				uri = merge(_)
				res = request(uri)
				if res.status_code[0] == '3':
					if res.headers['Location'].startswith(_) is True:
						return uri

		return False



def openredirect(target):
	re = OpenRedirection(target)
	payload = re.scan()
	return payload
