#!/usr/bin/python

from argparse import ArgumentParser
from os import getcwd
from os.path import abspath, isdir
from subprocess import Popen
from sys import stdin, stderr
from time import sleep
from urllib import urlencode
from urllib2 import urlopen, HTTPError

TIMEOUT_SECONDS = 5
SUCCESS_TEXT = 'Mysql configuration rows replaced to reflect a successful'

def print_body(body):
    stderr.write('Here is the response body: ')
    stderr.write(body)
    stderr.write('')

def start_server(args):
	server = Popen(['java', '-jar', 'jenkins-winstone.jar', '--warfile=wavsep.war',
	                '--useJasper', '-commonLibFolder=lib', 
	                '--httpPort={}'.format(args.http_port),
	                '--ajp13Port={}'.format(args.ajp13_port)])
	print 'Wavsep server process started with PID {}.'.format(server.pid)
	return server

def wait_for_enter(parser, server):
    print 'Press Enter to terminate.'
    stdin.read(1)
    server.terminate()
    parser.exit('Successful wavsep shutdown.')

def setup_server(server, parser, args):
	setup_params = {'username':args.mysql_user, 'password':args.mysql_pass,
		            'host':args.mysql_host, 'port':args.mysql_port,
		            'wavsep_username':'', 'wavsep_password':''}
	print 'Sending setup parameters: {}'.format(setup_params)
	sleep(TIMEOUT_SECONDS)
	installURL = \
		'http://localhost:{}/wavsep-install/install.jsp'.format(args.http_port)
	print 'Sending setup request to "{}"'.format(installURL)
	try:
		response = urlopen(installURL, urlencode(setup_params), 
							TIMEOUT_SECONDS)
		body = response.read()
		code = response.getcode()
	except HTTPError as http_error:
		body = http_error.reason
		code = http_error.code

	if code == 200:
	    print 'Got Success (200) response code from our setup request.'
	    if SUCCESS_TEXT in body:
	        print 'Wavsep setup request completed successully.'
	        wait_for_enter(parser, server)
	    else:
	    	print_body(body)
	    	server.terminate()
	    	parser.error(
	    		"Wavsep setup request didn't complete successfully.")
	else:
		print_body(body)
		server.terminate()
		parser.error('Unexpected response code to setup request: {}'.format(
			code))

parser = ArgumentParser(description ='''Launch and configure wavsep.
MySQL Server 5.5 will be used to create a database at 
{}/db'''.format(getcwd()))
parser.add_argument('--use-existing', action='store_true',
	                help='Use the already configured database.')
parser.add_argument('--mysql-user', type=str, nargs='?', 
	                default='root', help='MySQL Server admin user name',
	                metavar='USER')
parser.add_argument('--mysql-pass', type=str, nargs='?', default='',
                    help='MySQL Server admin password', metavar='PASS')
parser.add_argument('--mysql-host', type=str, nargs='?', default='localhost',
	                help='MySQL Server host (localhost is recommended)',
	                metavar='HOST')
parser.add_argument('--mysql-port', type=int, nargs='?', default='3306',
	                help='MySQL Server port')
parser.add_argument('--http-port', type=int, nargs='?', default='8080',
					help='Wavsep application HTTP port')
parser.add_argument('--ajp13-port', type=int, nargs='?', default='8009',
					help='Wavsep application AJP13 port')
args = parser.parse_args()
if args.use_existing:
    if isdir(abspath('db/WavsepConfigDB')):
	    server = start_server(args)
	    wait_for_enter(parser, server)
    else:
    	parser.error('No database found at {}/db'.format(getcwd()));
else:
    server = start_server(args)
    setup_server(server, parser, args)
