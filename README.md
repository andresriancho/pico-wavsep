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

It is possible to specify the listen ports using `--httpPort=8083 --ajp13Port=8084`.

For more options take a look at the [winstone documentation](http://winstone.sourceforge.net/#commandLine)

TODO
====
 * Need to further investigate how to [setup SQL engine for WAVSEP](https://github.com/andresriancho/pico-wavsep/issues/1)
