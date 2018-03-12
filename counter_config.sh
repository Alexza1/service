#!/bin/bash

# This script is about to configure the counter-service
# to be ready to run as a service in systemd on ubuntu os

# first copy the counter.service file to /etc/systemd/system/
# and set the relevant permission

chmod 744 counter.service
cp counter.service /etc/systemd/system/

echo counter.service copied to systemd
# reload the systemd daemon
systemctl daemon-reload

echo systemctl daemon-reload done
echo " "
echo ====================================================
echo ! counter-servicee is ready to be used as aservice !
echo ====================================================
echo " "
