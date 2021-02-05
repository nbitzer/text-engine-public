#!/bin/bash
set -x
DAEMON_PID=$(ps -ef | grep "daemon.py" | grep "sudo" | awk '{print $2}')
echo ${DAEMON_PID}
[[ -z ${DAEMON_PID} ]] || sudo kill ${DAEMON_PID}
sudo -E -u www-data python /home/ubuntu/flaskapp/daemon.py
sudo service apache2 restart
