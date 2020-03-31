from urllib.parse import urlparse,quote,unquote,parse_qs,parse_qsl
from core.URLMutator import URLMutator
from core.sendrequests import request_send
from utils.db import Database
from core.diff import diff_status_code,diff_headers,diff_text
from modules.code_valid import check_waf_rp
from utils.logger import logger

db = Database()
scan_logger = logger()


def judge(res):

	for i in range(len(res.history)):
		if "code" in res.history[i].headers['Location']:
			return urlparse(res.history[i].headers['Location']).query

	return False


def merge(re_part,redirect_uri):
	redirect_uri = quote(redirect_uri)
	query = parse_qs(re_part.query)
	
	redirect_list = []
	redirect_list.append(redirect_uri)
	query['redirect_uri'] = redirect_list

	
	new_query = ''
	for key,value in query.items():
		if new_query == '':
			new_query = new_query+key+'='+value[0]
		else:
			new_query = new_query+'&'+key+'='+value[0]

	return re_part._replace(query=new_query).geturl()

def valid_url(scanid,re_part,forge_url,vul,method,headers,body):
	info_code = ''
	for i in range(len(forge_url)):
		new_redirect = merge(re_part,forge_url[i])
		res = request_send(new_redirect,method,headers,body)
		if res == False:
			continue
		result = judge(res)
		if result:
			info_code = result
			print("%s[+]{0} is vulnerable to redirect attack%s".format(scanid)%(scan_logger.G,scan_logger.W))
			data = {"scanid":scanid,"url":re_part.geturl(),"type":"redirect","vul":"code leak","payload":new_redirect}
			db.insert_record("redirect",data)

	return info_code


def redirect_scan(scanid,url,method,headers,body=None):
	re_part=urlparse(url)
	redirect_uri = unquote(parse_qs(re_part.query)['redirect_uri'][0])
	malform_url = URLMutator(redirect_uri)

	auth_code =[]

	# scheme
	forge_url = malform_url.scheme_forge()
	code = valid_url(scanid,re_part,forge_url,"scheme of url",method,headers,body)
	auth_code.append(code)

	#userinfo 
	forge_url = malform_url.userinfo_forge()
	code = valid_url(scanid,re_part,forge_url,"userinfo of url",method,headers,body)
	auth_code.append(code)

	#domain
	forge_url = malform_url.domain_forge()
	code = valid_url(scanid,re_part,forge_url,"domain of url",method,headers,body)
	auth_code.append(code)

	#subdomain 
	forge_url = malform_url.subdomain_forge()
	code = valid_url(scanid,re_part,forge_url,"subdomain of url",method,headers,body)
	auth_code.append(code)

	#subdomain pop 
	subdomain = re_part.netloc.split('.')
	for i in range(len(subdomain)):
		forge_url = malform_url.subdomain_pop(i+1)
		code = valid_url(scanid,re_part,forge_url,"subdomain pop {num} of url".format(num=i),method,headers,body)
		auth_code.append(code)

	#pop_path
	path = re_part.path.split('/')
	for i in range(len(path)):
		forge_url = malform_url.pop_path(i+1)
		code = valid_url(scanid,re_part,forge_url,"path pop {num} of url".format(num=i),method,headers,body)
		auth_code.append(code)

	#query_forge
	forge_url = malform_url.query_forge()
	code = valid_url(scanid,re_part,forge_url,"query of url",method,headers,body)
	auth_code.append(code)

	#print(auth_code)
	for i in range(len(auth_code)):
		authorization_code = auth_code[i]
		if len(authorization_code) == 0:
			continue
		signal = check_waf_rp(scanid,url,method,headers,authorization_code)
		if signal == False:
			print("%s{0} is vulberable to the obtained token%s".format(scanid)%(scan_logger.G,scan_logger.W))
			data = {"scanid":scanid,"url":url,"type":"token check","vul":"the process of obtained token lack check","payload":url}
			db.insert_record("redirect",data)
			break





