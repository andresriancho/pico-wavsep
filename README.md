pico-wavsep
===========

A minimalistic way to run [wavsep](https://code.google.com/p/wavsep/)

```console
$ java -jar jenkins-winstone.jar --warfile=wavsep.war --useJasper --commonLibFolder=lib
[Winstone 2014/03/18 10:41:13] - Beginning extraction from war file
[Winstone 2014/03/18 10:41:14] - HTTP Listener started: port=8080
[Winstone 2014/03/18 10:41:15] - AJP13 Listener started: port=8009
[Winstone 2014/03/18 10:41:15] - Winstone Servlet Engine v0.9.10 running
```

Browse to [localhost:8080](http://localhost:8080) and you'll have access to WAVSEP.

Options
=======

It is possible to specify the listen ports using `--httpPort=8844 --ajp13Port=8845`.

For more options take a look at the [winstone documentation](http://winstone.sourceforge.net/#commandLine)

Easy Python Script
==================

_Requires Python 2.7+_

First, lets see what help is offered by the script:

```console
$ ./start.py --help
usage: start.py [-h] [--mysql-user [USER]] [--mysql-pass [PASS]]
                [--mysql-host [HOST]] [--mysql-port [MYSQL_PORT]]
                [--http-port [HTTP_PORT]] [--ajp13-port [AJP13_PORT]] [--out [OUT]]

Launch and configure wavsep. MySQL Server 5.5 will create a database at ./db

optional arguments:
  -h, --help            show this help message and exit
  --mysql-user [USER]   MySQL Server admin user name (default=root)
  --mysql-pass [PASS]   MySQL Server admin password (defaults to no password)
  --mysql-host [HOST]   MySQL Server host (default=localhost)
  --mysql-port [MYSQL_PORT]
                        MySQL Server port (default=3306)
  --http-port [HTTP_PORT]
                        Wavsep application HTTP port (default=8080)
  --ajp13-port [AJP13_PORT]
                        Wavsep application AJP13 port (default=8009)
  --out [OUT]           File to wavsep server stdout to (default=pico-wavsep.log)
```

Notice that wavsep will be needing MySQL 5.5 to be installed on your system.
On my system this was accomplished with
`sudo apt-get install mysql-server-5.5`.

Let's see what happens if we just launch the script with no arguments, not
having previously installed the wavsep database.

```console
$ ./start.py 
usage: start.py [-h] [--mysql-user [USER]] [--mysql-pass [PASS]]
                [--mysql-host [HOST]] [--mysql-port [MYSQL_PORT]]
                [--http-port [HTTP_PORT]] [--ajp13-port [AJP13_PORT]] [--out [OUT]]
start.py: error: No "db" directory found. Please provide at least one explicit --mysql-* argument.
```

The script knows I've never installed the wavsep database before. Let's explicitly provide 
the MySQL root password, to signal the script that we wish to do this:

```console
$ ./start.py --mysql-pass 'Pa$$w0rd'
Wavsep server process started with PID 6012.
Server normal messages are being sent to pico-wavsep.log
Server error messages are being sent to pico-wavsep_err.log
Waiting a moment for server to initialize.
Wavsep setup request completed successully.
```

Success! To shut down the server, press CTRL-C.

In the above session, wavsep started _and_ installed its database
successfully. At that point, `start.py` also created a special file, `wavsep-installed.txt`, which
is the indicator that future invocations don't need to be provided installation parameters. Hitting
Enter shuts the server down. The next time, it is not necessary to provide
any arguments.

```console
$ ./start.py 
Wavsep server process started with PID 6063.
Server normal messages are being sent to pico-wavsep.log
Server error messages are being sent to pico-wavsep_err.log
``` 