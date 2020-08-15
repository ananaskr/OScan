## Description
This is a tool for scanning the vulnerabilities of the OAuth2.0 implementations on the web.

## Done

- [x] CSRF.
- [x] Scope Privilege Escalation.
- [x] Covert Redirection.
- [x] Open Redirection.
- [x] Same Original Redirection with Referer.
- [x] Authorization Code Middle Attack.
- [x] Access Token Middle Attack.

## Todo
- [] Same Original Redirection with XSS.

## Install

[1] Start the server of mongodb 

```
mongod --dbpath /yourpath
```

[2] Install the requirements

```
pip3 install -r requirements.txt
```


## Usage

3. exec the command

```
python3 oscan.py -req1 requests1 -req2 requests2
```

### Example

