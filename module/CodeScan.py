from urllib.parse import urlparse,quote,unquote,parse_qs,parse_qsl

db = Database()

# This is used for checking whether authorization code. 
class CodeScan(object):

	def __init__(self):
		pass

	# To fetch a valid code, ensure the code has not been used.
	def fetch_code(self):




	def check_waf_rp(scanid,url,method,headers,auth_code):
		res = request_send(url,method,headers)
		res1 = request_send(url,method,headers)
		code_url = ''
		for i in range(len(res.history)):
			if "code" in res.history[i].headers['Location']:
				code_url = res.history[i].headers['Location']
				break

		if code_url != '':
			re_parts = urlparse(code_url)
			new_query = []
			new_query.append(auth_code)
			new_code_url = re_parts._replace(query=auth_code).geturl()
			res_new = request_send(new_code_url,method,headers)

			if diff_status_code(res,res_new):
				pass
				return True
			else:
				if diff_headers(res,res1,res_new):
					pass
					return True
				else:
					if diff_text(res,res1,res_new):
						pass
						return True
					else:
						return False

def scancode(task):

	scan = CodeScan(task.target1)



	


