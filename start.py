#!/usr/bin/python

TIMEOUT_SECONDS = 5
WAVSEP_PORT = 8844
AJP13_PORT = 8845
SUCCESS_TEXT = 'Mysql configuration rows replaced to reflect a successful'

def print_body(body):
    print "Here's the response body: "
    print body

from os import getcwd

installURL = \
    'http://localhost:{}/wavsep-install/install.jsp'.format(WAVSEP_PORT)
message = '''Welcome to pico-wavsep. Here are some instructions to properly
configure your wavsep instance:

1. Make sure you have MySQL 5.5 installed, noting the db admin username and
   password.
2. A database will be created in "{}/db".
3. Browse to "{}".
4. Enter the previously noted db admin credentials in the form.
'''.format(getcwd(), installURL)

print message

from subprocess import Popen

server = Popen(['java', '-jar', 'jenkins-winstone.jar', '--warfile=wavsep.war',
                '--useJasper', '-commonLibFolder=lib', 
                '--httpPort={}'.format(WAVSEP_PORT),
                '--ajp13Port={}'.format(AJP13_PORT)])

print 'Wavsep server process started with PID {}.'.format(server.pid)

from urllib import urlencode

data = urlencode({'username':'root', 'password':'Pa$$w0rd',
	              'host':'localhost', 'port':'3306', 'wavsep_username':'',
	              'wavsep_password':''})

from urllib2 import urlopen,HTTPError
from sys import stdin
from time import sleep

sleep(5)
print 'Sending setup request to "{}"'.format(installURL)
try:
    response = urlopen(installURL, data, TIMEOUT_SECONDS)
    body = response.read()
    code = response.getcode()
except HTTPError as http_error:
	body = http_error.reason
	code = http_error.code

if code == 200:
    print 'Got Success (200) response code from our setup request.'
    if SUCCESS_TEXT in body:
        print 'Wavsep setup request completed successully.'
        print 'Press Enter to terminate.'
        stdin.read(1)
    else:
    	print "Wavsep setup request didn't complete successfully."
    	print_body(body);
else:
	print "Didn't get expected response code to setup request: {}".format(
		code)
	print_body(body);

server.terminate()