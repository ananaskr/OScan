import requests

from utils.Cookie import get_cookie

requests.packages.urllib3.disable_warnings()
cookie_jar = get_cookie()


def request_send(url,method,headers,body=None):

	user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
	headers["User-Agent"] = user_agent
	try:
		if method.upper() == "GET":
			result = requests.get(url,headers=headers,cookies=cookie_jar,allow_redirects=True,verify=False)
		elif method.upper() == "POST":
			result = requests.post(url,headers=headers,cookies=cookie_jar,json=body,allow_redirects=True,verify=False)
		elif method.upper() == "PUT":
			result = requests.put(url,headers=headers,cookies=cookie_jar,data=body,allow_redirects=True,verify=False)
		elif method.upper() == "OPTIONS":
			result = requests.options(url,headers=headers,verify=False)

		return result
	except Exception as e:
		return False


