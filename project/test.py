from diff import diff_status_code,diff_headers,diff_text
from sendrequests import request_send
import time


url = "https://api.weibo.com/oauth2/authorize?client_id=1881139527&redirect_uri=http%3A%2F%2Fwww.jianshu.com%2Fusers%2Fauth%2Fweibo%2Fcallback&response_type=code&state=%257B%257D"
headers={}
res1 = request_send(url,"get",headers=headers)
print(res1.text)

res2 = request_send(url,"get",headers=headers)

url2 = "https://www.jianshu.com/users/auth/weibo/callback?state=%7B%7D&code=123362a45e08548cb79651537346f5f8"
res3 = request_send(url2,"get",headers=headers)

res = diff_text(res1,res2,res3)
print(res)





