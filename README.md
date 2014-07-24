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
usage: start.py [-h] [--use-existing] [--mysql-user [USER]] [--mysql-pass [PASS]] [--mysql-host [HOST]] [--mysql-port [MYSQL_PORT]] [--http-port [HTTP_PORT]]
                [--ajp13-port [AJP13_PORT]]

Launch and configure wavsep. MySQL Server 5.5 will be used to create a database at /home/dale/Documents/git/pico-wavsep/db

optional arguments:
  -h, --help            show this help message and exit
  --use-existing        Use the already configured database.
  --mysql-user [USER]   MySQL Server admin user name (default=root)
  --mysql-pass [PASS]   MySQL Server admin password (defaults to no password)
  --mysql-host [HOST]   MySQL Server host (default=localhost)
  --mysql-port [MYSQL_PORT]
                        MySQL Server port (default=3306)
  --http-port [HTTP_PORT]
                        Wavsep application HTTP port (default=8080)
  --ajp13-port [AJP13_PORT]
                        Wavsep application AJP13 port (default=8009)

```

Notice that wavsep will be needing MySQL 5.5 to be installed on your system.
On my system this was accomplished with
`sudo apt-get install mysql-server-5.5`.

Let's see what happens if we just launch the script with no arguments, not
having previously "installed" the wavsep database.

```console
$ ./start.py
Wavsep server process started with PID 11738.
Server normal messages are being sent to /home/dale/Documents/git/pico-wavsep/pico-wavsep.log
Server error messages are being sent to /home/dale/Documents/git/pico-wavsep/pico-wavsep_err.log
Waiting a moment for server to initialize.
Sending setup request to http://localhost:8080/wavsep-install/install.jsp
with parameters {'username': 'root', 'wavsep_password': '', 'host': 'localhost', 'wavsep_username': '', 'password': '', 'port': 3306}
Got Success (200) response code from our setup request.
usage: start.py [-h] [--use-existing] [--mysql-user [USER]] [--mysql-pass [PASS]] [--mysql-host [HOST]] [--mysql-port [MYSQL_PORT]] [--http-port [HTTP_PORT]]
                [--ajp13-port [AJP13_PORT]]
start.py: error: Expected to see this in response: "Mysql configuration rows replaced to reflect a successful installation"
```

It turns out that not all steps could be completed. If you inspect the
`pico-wavsep*.log` files, Wavsep isn't very helpful, but it turns out that
the problem in this case is that I didn't provide the password, which I had
rather creatively set to `Pa$$w0rd`. Let's do that:

```console
$ ./start.py --mysql-pass "Pa\$\$w0rd"
Wavsep server process started with PID 3387.
Server normal messages are being sent to /home/dale/Documents/git/pico-wavsep/pico-wavsep.log
Server error messages are being sent to /home/dale/Documents/git/pico-wavsep/pico-wavsep_err.log
Waiting a moment for server to initialize.
Sending setup request to http://localhost:8080/wavsep-install/install.jsp
with parameters {'username': 'root', 'wavsep_password': '', 'host': 'localhost', 'wavsep_username': '', 'password': 'Pa$$w0rd', 'port': 3306}
Got Success (200) response code from our setup request.
Wavsep setup request completed successully.
Saving parameters to args.pickle
Press Enter to terminate.

Successful wavsep shutdown.
```

In the above session, Wavsep started _and_ installed its database
successfully. At that point, it saved the parameters for future use. I had to
hit Enter to shut the server down. The next time, it is possible to give the
`--use-existing` flag:


```console
$ ./start.py --use-existing
Loading parameters from args.pickle
Wavsep server process started with PID 3542.
Server normal messages are being sent to /home/dale/Documents/git/pico-wavsep/pico-wavsep.log
Server error messages are being sent to /home/dale/Documents/git/pico-wavsep/pico-wavsep_err.log
Waiting a moment for server to initialize.
Sending setup request to http://localhost:8080/wavsep-install/install.jsp
with parameters {'username': 'root', 'wavsep_password': '', 'host': 'localhost', 'wavsep_username': '', 'password': 'Pa$$w0rd', 'port': 3306}
Got Success (200) response code from our setup request.
Wavsep setup request completed successully.
Saving parameters to args.pickle
Press Enter to terminate.

Successful wavsep shutdown.
```