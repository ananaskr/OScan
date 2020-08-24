<p align="center">
  <a href="https://github.com/ananaskr/OScan">
    <img src="https://github.com/ananaskr/OScan/blob/master/img/2.png"
    alt="OScan logo">
  </a>
</p>

<p align="center">
  OAuth Web Application Security Scanner
  <br>
</p>

<p align="center">
  <a target="_blank"><img src="https://img.shields.io/badge/release-v1.0%20beta-blue"></a>
  <a target="_blank"><img src="https://img.shields.io/badge/python-3.6.0-blue"></a>
</p>

## Description
This is a tool for scanning the vulnerabilities of the OAuth2.0 implementations on the web. According to the multipart (ie, Client, User, Authorization Server and Resource Server) interations, serveral attacks has been divided.

## Prerequisites

Install and start the server of mongodb. 

```
mongod -dbpath /tmp/mongodata/ -logpath /tmp/mongodata/mongo.log -logappend -fork -port 27017
```

Install the requirements.

```
pip install -r requirements.txt
```


## Done

- [x] CSRF.
- [x] Scope Privilege Escalation.
- [x] Open Redirection.
- [x] Same Original Redirection with Referer.
- [x] Authorization Code Middle Attack.


## Todo
- [ ] Covert Redirection.
- [ ] Same Original Redirection with XSS.
- [ ] Access Token Middle Attack.
- [ ] Same Original Redirection with remote image.
- [ ] OAuth API Crawing.



## Usage

Use `-h` options to see all the usage.


The API to be detected is best given in the following JSON format. If you think it is complex, you can also provide only one url with `-u` options instead. It will consume more time and get a false negative result. 
![](https://github.com/ananaskr/OScan/blob/master/img/1.png)
exec the command

```
python oscan.py -r example.json
python oscan.py -u http://api.xxx.com/xxx
```

## Example
![](https://github.com/ananaskr/OScan/blob/master/img/4.png)

## OAuth API
In [https://en.wikipedia.org/wiki/List\_of\_OAuth\_providers](https://en.wikipedia.org/wiki/List_of_OAuth_providers) sumarizes many oauth provider. The corresponding OAuth API prefix can be extracted to identify OAuth APIs in websites.  

data/provider.txt 


| OAuth Provider | OAuth API format |
| :-------------- | :---------------- |
|  500px         | 	api.500px.com/v1/oauth/request_token |
| Amazon|www.amazon.com/ap/oa|
|AOL|api.login.aol.com/oauth2/request_auth|
|Autodesk|developer.api.autodesk.com/authentication/v1/authorize|
|Basecamp|launchpad.37signals.com/authorization/new|
|Battle.net|battle.net/oauth/authorize|www.battlenet.com.cn/oauth/authorize|
|Bitbucket|bitbucket.org/site/oauth2/authorize|
|Facebook|www.facebook.com/v3.1/dialog/oauth|
|GitHub|github.com/login/oauth/authorize|
|Google|accounts.google.com/signin/oauth|
|Sina Weibo|	api.weibo.com/oauth2/authorize|
|...|...|
