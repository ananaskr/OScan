
from config.config import get_file
from urllib.parse import urlparse,quote,unquote,parse_qs,parse_qsl

# URLMutator class provide many ways to mutate url include: [scheme, userinfo, domain, subdomain, path, query]
class URLMutator(object):

	def __init__(self,url):
		self.url = url
		self.reparts = urlparse(url)

	# Malform of scheme.
	def scheme_forge(self):
		scheme_orgin = self.reparts.scheme
		schemes = get_file('scheme.txt')
		forge_url = []
		for scheme in schemes:
			if scheme != scheme_orgin:
				forge_url.append(self.reparts._replace(scheme=scheme).geturl())
		
		#remove the scheme
		#print(self.url)
		forge_url.append(self.url.split(':',1)[1])

		return forge_url

	# Malform of userinfo.
	def userinfo_forge(self):
		forge_url = []
		if self.reparts.username is None and self.reparts.password is None:
			domain = "www.baidu.com"+"@"+self.reparts.netloc
			forge_url.append(self.reparts._replace(netloc=domain).geturl())
		else:
			domain = "abc"+self.reparts.netloc
			forge_url.append(self.reparts._replace(netloc=domain).geturl())

		return forge_url

	# Malform of domain.
	def domain_forge(self):
		forge_url = []
		# suffix match
		domain = 'abc'+ self.reparts.netloc
		forge_url.append(self.reparts._replace(netloc=domain).geturl())
		domain = self.reparts.netloc +'.cc'
		forge_url.append(self.reparts._replace(netloc=domain).geturl())
		domain = "www.baidu.com"
		forge_url.append(self.reparts._replace(netloc=domain).geturl())

		return forge_url

	# Malform of subdomain.
	def subdomain_add(self):
		forge_url = []
		subdomain = "abc."
		domain = self.reparts.netloc
		if domain.startswith("www"):
			new_domain = subdomain+domain[3:]
		else:
			new_domain = subdomain+domain

		forge_url.append(self.reparts._replace(netloc=new_domain).geturl())
		
		return forge_url

	# Malform of subdomain by pop.
	def subdomain_pop(self,num=1):
		forge_url = []
		domain=self.reparts.netloc
		parts=domain.split('.')
		if len(parts)-num >= 2:
			domain='.'.join(parts[num:])
			forge_url.append(self.reparts._replace(netloc=domain).geturl())
		else:
			print(f'cannot pop {num} subdomains')
			return False
		
		return forge_url

	# Malform of path by pop
	def path_pop(self,num=1):
		forge_url = []
		path=self.reparts.path
		print(path)
		paths=path.split('/')
		if len(paths)-num >=0:
			path='/'.join(paths[:-num])
			forge_url.append(self.reparts._replace(path=path).geturl())
		else:
			print(f'cannot pop {num} paths')
			return ''
		return forge_url

	# Malform of query.
	def query_forge(self):
		forge_url = []
		forge_url.append(self.reparts._replace(query='').geturl())
		query = self.re_parts.query
		if query:
			to_append = '&'+'xyz=2717'
		else:
			to_append = 'xyz=2717'
		query = query+to_append
		forge_url.append(self.reparts._replace(query=query).geturl())

		return forge_url

# The main function to get malformed uris.
# @Return <List> the collection of malformed uris.
def url_mutate(url):
	uris = []
	if isinstance(url,str):
		mutator = URLMutator(url)
	else:
		mutator = URLMutator(url[0])
	uris = uris + mutator.scheme_forge()
	uris = uris + mutator.domain_forge()
	uris = uris + mutator.userinfo_forge()
	uris = uris + mutator.subdomain_add()
	#uris = uris + query_forge()
	'''
	i = 0
	while True:
		i += 1
		muris = subdomain_pop(i)
		if not muris:
			break
		uris = uris + muris
	i = 0
	while True:
		i += 1
		muris = path_pop(i)
		if not muris:
			break
		uris = uris + muris
	'''
	return uris