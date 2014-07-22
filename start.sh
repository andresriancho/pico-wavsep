#!/bin/bash

WAVSEP_PORT=8844
AJP13_PORT=8845
echo "Welcome to pico-wavsep. Here are some instructions to properly
configure your wavsep instance:

1. Make sure you have MySQL 5.5 installed, noting the db admin username and
   password.
2. A database will be created in \"$HOME/db\".
3. Browse to http://localhost:$WAVSEP_PORT/wavsep/wavsep-install/install.jsp
4. Enter the previously noted db admin credentials in the form.
"
java -jar jenkins-winstone.jar --warfile=wavsep.war --useJasper \
     --commonLibFolder=lib --httpPort=$WAVSEP_PORT --ajp13Port=$AJP13_PORT