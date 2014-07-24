#!/usr/bin/python

from argparse import ArgumentParser
from os import getcwd
from os.path import abspath, isdir, isfile
from pickle import load, dump
from subprocess import Popen
from sys import stdin, stderr
from time import sleep
from urllib import urlencode
from urllib2 import urlopen, HTTPError

TIMEOUT_SECONDS = 5
SUCCESS_TEXT = 'Mysql configuration rows replaced to reflect a successful installation'

def print_body(body):
    server_out.write('Here is the response body: ')
    server_out.write(body)
    server_out.write('')

def start_server(args):
	server = Popen(['java', '-jar', 'jenkins-winstone.jar', '--warfile=wavsep.war',
	                '--useJasper', '-commonLibFolder=lib', 
	                '--httpPort={}'.format(args.http_port),
	                '--ajp13Port={}'.format(args.ajp13_port)], stdout=server_out,
	                stderr=server_err)
	print 'Wavsep server process started with PID {}.'.format(server.pid)
	print 'Server normal messages are being sent to {}/{}'.format(getcwd(), fn_out)
	print 'Server error messages are being sent to {}/{}'.format(getcwd(), fn_err)
	return server

def setup_server(server, parser, args, fn_args):
	print('Waiting a moment for server to initialize.')
	sleep(TIMEOUT_SECONDS)
	installURL = \
		'http://localhost:{}/wavsep-install/install.jsp'.format(args.http_port)
	print 'Sending setup request to {}'.format(installURL)
	setup_params = {'username':args.mysql_user, 'password':args.mysql_pass,
		            'host':args.mysql_host, 'port':args.mysql_port,
		            'wavsep_username':'', 'wavsep_password':''}
	print 'with parameters {}'.format(setup_params)
	try:
		response = urlopen(installURL, urlencode(setup_params), 
							TIMEOUT_SECONDS)
		body = response.read()
		code = response.getcode()
	except HTTPError as http_error:
		body = http_error.reason
		code = http_error.code

	print_body(body)
	if code == 200:
	    print 'Got Success (200) response code from our setup request.'
	    if SUCCESS_TEXT in body:
	        print 'Wavsep setup request completed successully.'
	        print 'Saving parameters to {}'.format(fn_args)
	        with open(fn_args, 'w') as argsfile:
	        	dump(args, argsfile)
    		print 'Press Enter to terminate.'
    		try:
    			stdin.read(1)
    		finally:
    			server.terminate()
    			parser.exit('Successful wavsep shutdown.')
	    else:
	    	server.terminate()
	    	parser.error('Expected to see this in response: "{}"'.format(SUCCESS_TEXT))
	else:
		server.terminate()
		parser.error('Unexpected response code to setup request: {}'.format(
			code))

parser = ArgumentParser(description ='''Launch and configure wavsep.
MySQL Server 5.5 will be used to create a database at 
{}/db'''.format(getcwd()))
parser.add_argument('--use-existing', action='store_true',
	                help='Use the already configured database.')
parser.add_argument('--mysql-user', type=str, nargs='?', 
	                default='root', metavar='USER',
	                help='MySQL Server admin user name (default=root)')
parser.add_argument('--mysql-pass', type=str, nargs='?', default='',
                    help='MySQL Server admin password (defaults to no password)',
                    metavar='PASS')
parser.add_argument('--mysql-host', type=str, nargs='?', default='localhost',
	                help='MySQL Server host (default=localhost)',
	                metavar='HOST')
parser.add_argument('--mysql-port', type=int, nargs='?', default='3306',
	                help='MySQL Server port (default=3306)')
parser.add_argument('--http-port', type=int, nargs='?', default='8080',
					help='Wavsep application HTTP port (default=8080)')
parser.add_argument('--ajp13-port', type=int, nargs='?', default='8009',
					help='Wavsep application AJP13 port (default=8009)')
args = parser.parse_args()
fn_args = 'args.pickle'
fn_out = 'pico-wavsep.log'
fn_err = 'pico-wavsep_err.log'
server_out = open(fn_out, 'w')
server_err = open(fn_err, 'w')
if args.use_existing:
    if isfile(abspath(fn_args)):
	    with open(fn_args) as argsfile:
	    	print 'Loading parameters from {}'.format(fn_args)
	    	args = load(argsfile)
    else:
    	parser.error("You can't invoke --use-existing when you have no previous sessions.");

server = start_server(args)
setup_server(server, parser, args, fn_args)
