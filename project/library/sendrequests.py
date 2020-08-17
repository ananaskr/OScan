import requests


requests.packages.urllib3.disable_warnings()

# This class is a capsulation for sending requests.
class ORequest(object):

	def __init__(self,target):
		self.target = target

	# Check whether headers or method is provided before requests.
	def check(self):
		if 'headers' not in self.target or self.target['headers'] == '':
		#if not self.target.has_key('headers') | self.target['headers'] == '':
			self.target['headers'] = {
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
			}
		if 'method' not in self.target or self.target['method'] == '':
		#if not self.target.has_key('method') | self.target['method'] == '':
			self.target['method'] = 'GET'
		if 'cookies' not in self.target:
			self.target['cookies'] = ''

	# The function to send requests according to method
	def request_send(self):
		if self.target['method'].upper() == "GET":
			result = requests.get(url=self.target['url'], headers=self.target['headers'], cookies=self.target['cookies'], allow_redirects=True, verify=False)
		elif self.target['method'].upper() == "POST":
			result = requests.post(self.target['url'],headers=self.target['headers'],cookies=self.target['cookies'],data=self.target['data'],allow_redirects=True,verify=False)
		elif self.target['method'].upper() == "PUT":
			result = requests.put(self.target['url'],headers=self.target['headers'],cookies=self.target['cookies'],data=self.target['data'],allow_redirects=True,verify=False)
		elif self.target['method'].upper() == "OPTIONS":
			result = requests.options(self.target['url'],headers=self.target['headers'],verify=False)
		else:
			result = False
		return result


# The Interface exposed to others for calling.
def request(target):
	req = ORequest(target)
	req.check()
	result = req.request_send()
	if not result:
		print("request to target has come to error.")
		return False
	return result

