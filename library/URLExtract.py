from urllib.parse import urlparse,quote,unquote,parse_qs,parse_qsl
from bs4 import BeautifulSoup

class URLExtract(object):

	def __init__(self,url,target):
		self.target = BeautifulSoup(target,'html.parser')
		self.url = url

	# Extract some same origin 
	def extract_same_url(self):
		url = []
		tag = self.target.select('a')
		for _ in tag:
			
			domain1 = urlparse(_['href']).netloc
			domain2 = urlparse(self.url).netloc
			if (domain1 == domain2) and (_['href'] != self.url):
				url.append(_['href'])

		return url


def urlextract(url,target):
	#print(target.content)
	extractor = URLExtract(url,target.content)
	urls = extractor.extract_same_url() 
	if len(urls) >= 1:
		return urls
	


