
from utils.config import get_list
from urllib.parse import urlparse,quote,unquote,parse_qs,parse_qsl


class URLMutator(object):
	def __init__(self,re_url):
		self.re_url = re_url
		self.re_parts = urlparse(self.re_url)

	# the malform of the scheme
	def scheme_forge(self):
		scheme_orgin = self.re_parts.scheme
		schemes = get_list('url.property','url','scheme')
		forge_url = []
		for scheme in schemes:
			if scheme != scheme_orgin:
				forge_url.append(self.re_parts._replace(scheme=scheme).geturl())
		
		#remove the scheme
		forge_url.append(self.re_url.split(':',1)[1])

		return forge_url


	def userinfo_forge(self):
		forge_url = []
		if self.re_parts.username is None and self.re_parts.password is None:
			domain = "www.baidu.com"+"@"+self.re_parts.netloc
			forge_url.append(self.re_parts._replace(netloc=domain).geturl())
		else:
			domain = "abc"+self.re_parts.netloc
			forge_url.append(self.re_parts._replace(netloc=domain).geturl())

		return forge_url

	def domain_forge(self):
		forge_url = []
		# suffix match
		domain = 'abc'+ self.re_parts.netloc
		forge_url.append(self.re_parts._replace(netloc=domain).geturl())
		domain = self.re_parts.netloc +'.cc'
		forge_url.append(self.re_parts._replace(netloc=domain).geturl())
		domain = "www.baidu.com"
		forge_url.append(self.re_parts._replace(netloc=domain).geturl())

		return forge_url

	def subdomain_forge(self):
		forge_url = []
		subdomain = "abc."
		domain = self.re_parts.netloc
		if domain.startswith("www"):
			new_domain = subdomain+domain[3:]
		else:
			new_domain = subdomain+domain

		forge_url.append(self.re_parts._replace(netloc=new_domain).geturl())
		
		return forge_url

	def subdomain_pop(self,num=1):
		forge_url = []
		domain=self.re_parts.netloc
		parts=domain.split('.')
		if len(parts)-num >= 2:
			domain='.'.join(parts[num:])
			forge_url.append(self.re_parts._replace(netloc=domain).geturl())
		else:
			print(f'cannot pop {num} subdomains')
		
		return forge_url

	def pop_path(self,num=1):
		forge_url = []
		path=self.re_parts.path
		print(path)
		paths=path.split('/')
		if len(paths)-num >=0:
			path='/'.join(paths[:-num])
			forge_url.append(self.re_parts._replace(path=path).geturl())
		else:
			print(f'cannot pop {num} paths')
		return forge_url

	def query_forge(self):
		forge_url = []
		forge_url.append(self.re_parts._replace(query='').geturl())
		query = self.re_parts.query
		if query:
			to_append = '&'+'xyz=2717'
		else:
			to_append = 'xyz=2717'
		query = query+to_append
		forge_url.append(self.re_parts._replace(query=query).geturl())

		return forge_url

