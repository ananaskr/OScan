import json

from modules.csrf import csrf_scan
from modules.redirect import redirect_scan
from core.bodyformat import body2json
#import scope_scan


def oauth_scan(scanid,url1,method,headers1,body1,url2,headers2,body2):

	#headers1 = json.loads(headers1)
	#headers2 = json.loads(headers2)
	if method == "POST":
		body1 = body2json(headers1,body1)
		body2 = body2json(headers2,body2)

	print("starting scan the csrf vulnerability..................")
	csrf_scan(scanid,url1,method,headers1,body1,url2,headers2,body2)

	print("starting scan the redirect vulnerability..................")
	redirect_scan(scanid,url1,method,headers1,body1)
	#scope_scan.scope_scan(scanid,url1,method,headers1,body1)




	


