import json

'''
text/html
text/plain
text/xml

image/gif
image/jpeg
image/png

application/xhtml+xml
application/xml
application/atom+xml
application/json
application/pdf
application/msword
application/octet-stream
application/x-www-form-urlencoded

multipart/form-data

'''

def body2json(header,body):
	if header['content-type'] != 'application/json':
		new_body = {}
		body_list = body.split('&')
		for i in range(len(body_list)):
			param = body_list.split('=')
			new_body[param[0]]=param[1]
		return new_body
	else:
		return body

def json2raw(header,body):
	if header['content-type'] == 'text/plain':
		body_list=[]
		for key,value in body.items():
			body_list.append(key+'='+value)

		raw_body = '&'.join(body_list)
		return raw_body
	else:
		return body
