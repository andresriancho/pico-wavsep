#!/usr/bin/python

from os import environ

HOME = environ['HOME']
WAVSEP_PORT = 8844
AJP13_PORT = 8845
message = '''Welcome to pico-wavsep. Here are some instructions to properly
configure your wavsep instance:

1. Make sure you have MySQL 5.5 installed, noting the db admin username and
   password.
2. A database will be created in "{}/db".
3. Browse to http://localhost:{}/wavsep/wavsep-install/install.jsp
4. Enter the previously noted db admin credentials in the form.
'''.format(HOME, WAVSEP_PORT)

print message

from subprocess import call,CalledProcessError
try:
    call(['java', '-jar', 'jenkins-winstone.jar', '--warfile=wavsep.war',
	      '--useJasper', '-commonLibFolder=lib', 
	      '--httpPort={}'.format(WAVSEP_PORT),
	      '--ajp13Port={}'.format(AJP13_PORT)])
except KeyboardInterrupt as ki:
	print "Process was interrupted (likely by CTRL+C)."
except CalledProcessError as cpe:
	print "Exited Java process with exit code: {}".format(cpe.returncode)