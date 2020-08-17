import json

from requests.cookies import RequestsCookieJar

cookie_jar = RequestsCookieJar()

def get_cookie():
	with open('cookie.txt') as f:
		cookies = f.read()

	for cookie in json.loads(cookies):
		cookie_jar.set(cookie['name'],cookie['value'])

	return cookie_jar