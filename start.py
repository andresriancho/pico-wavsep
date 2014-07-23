#!/usr/bin/python

WAVSEP_PORT = 8844
AJP13_PORT = 8845

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
print
print 'Press any key to terminate.'

from sys import stdin

stdin.read(1)
server.terminate()