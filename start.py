#!/usr/bin/python

from __future__ import print_function

from argparse import ArgumentParser
from os.path import abspath, isfile
from pickle import load, dump
from subprocess import CalledProcessError, Popen
from sys import argv
from time import sleep
from urllib import urlencode
from urllib2 import urlopen, HTTPError

import logging

logging.basicConfig(filename='start.log', level=logging.DEBUG)

TIMEOUT_SECONDS = 5
SUCCESS_TEXT = ('Mysql configuration rows replaced to reflect a successful'
                ' installation')


def handle_setup_result(body, server_out):
    server_out.write('Here is the response body: ')
    server_out.write(body)
    server_out.write('')


def start_server(args, server_out, server_err, fn_out, fn_err):
    server = Popen(['java', '-jar', 'jenkins-winstone.jar', 
                    '--warfile=wavsep.war', '--useJasper',
                    '-commonLibFolder=lib', 
                    '--httpPort={}'.format(args.http_port),
                    '--ajp13Port={}'.format(args.ajp13_port)],
                   stdout=server_out,
                   stderr=server_err)
    
    print('WAVSEP server process started with PID {}.'.format(server.pid))
    print('Server normal messages are being sent to {}'.format(fn_out))
    print('Server error messages are being sent to {}'.format(fn_err))

    print('Waiting a moment for server to initialize.')
    sleep(TIMEOUT_SECONDS)

    port = args.http_port
    url = 'http://localhost:{}/'.format(port)
    print('WAVSEP is running at %s' % url)

    return server


def install_db(server, parser, args, fn_flag, server_out):
    port = args.http_port
    install_url = 'http://localhost:{}/wavsep-install/install.jsp'.format(port)

    logging.debug('Sending setup request to {}'.format(install_url))
    setup_params = {'username': args.mysql_user,
                    'password': args.mysql_pass,
                    'host': args.mysql_host,
                    'port': args.mysql_port,
                    'wavsep_username': '',
                    'wavsep_password': ''}

    logging.debug('with parameters {}'.format(setup_params))
    try:
        response = urlopen(install_url,
                           urlencode(setup_params),
                           TIMEOUT_SECONDS)
        body = response.read()
        code = response.getcode()
    except HTTPError as http_error:
        body = http_error.reason
        code = http_error.code

    handle_setup_result(body, server_out)
    if code == 200:
        logging.debug('Got Success (200) response code from our setup request.')

        if SUCCESS_TEXT in body:
            print('WAVSEP setup request completed successfully.')
            logging.debug('Saving install flag.')
            with open(fn_flag, 'w') as flagfile:
                dump(True, flagfile)
        else:
            server.terminate()
            msg = 'Expected to see this in response: "{}"'.format(SUCCESS_TEXT)
            parser.error(msg)
    else:
        server.terminate()
        msg = 'Unexpected response code to setup request: {}'.format(code)
        parser.error(msg)


def main():
    parser = ArgumentParser(description='Launch and configure WAVSEP to use'
                                        ' MySQL server.')

    parser.add_argument('--mysql-user', type=str, nargs='?', default='root',
                        metavar='USER',
                        help='MySQL Server admin user name (default=root)')
    
    parser.add_argument('--mysql-pass', type=str, nargs='?', default='',
                        const='', metavar='PASS',
                        help='MySQL root password (defaults to no password)')
    
    parser.add_argument('--mysql-host', type=str, nargs='?',
                        default='localhost', const='localhost', metavar='HOST',
                        help='MySQL Server host (default=localhost)')
    
    parser.add_argument('--mysql-port', type=int, nargs='?', default='3306',
                        help='MySQL Server port (default=3306)', const='3306')
    
    parser.add_argument('--http-port', type=int, nargs='?', default='8080',
                        help='WAVSEP application HTTP port (default=8080)',
                        const='8080')
    
    parser.add_argument('--ajp13-port', type=int, nargs='?', default='8009',
                        help='WAVSEP application AJP13 port (default=8009)',
                        const='8009')
    
    fn_out = 'pico-wavsep.log'
    fn_flag = 'wavsep-installed.txt'
    _help = 'File to WAVSEP server stdout to (default={})'.format(fn_out)
    parser.add_argument('--out', type=str, nargs='?',
                        default=fn_out, help=_help)
    
    args = parser.parse_args()
    install = ' '.join(argv[1:]).find('--mysql') >= 0
    logging.debug('Install Server? {}'.format(install))

    if not install:
        previous = False
        if isfile(abspath(fn_flag)):
            with open(fn_flag) as flagfile:
                logging.debug('Loading parameters from {}'.format(fn_flag))
                previous = load(flagfile)
        logging.debug('Previous install detected? {}'.format(previous))
        if not previous:
            parser.error('No "db" directory found. Please provide at least'
                         ' one explicit --mysql-* argument.')
    
    fn_out = args.out
    fn_err = 'pico-wavsep_err.log'
    server_out = open(fn_out, 'w')
    server_err = open(fn_err, 'w')
    server = None
    
    try:
        server = start_server(args, server_out, server_err, fn_out, fn_err)
        if install:
            install_db(server, parser, args, fn_flag, server_out)
        server.wait()
    except KeyboardInterrupt:
        logging.debug('Keyboard interrupt (likely CTRL-C.')
    except CalledProcessError as cpe:
        msg = 'Exited Java process with exit code: {}'.format(cpe.returncode)
        logging.debug(msg)
    finally:
        if server is not None:
            logging.info('Attempting to shut down server.')
            server.terminate()


if __name__ == '__main__':
    main()