#!/usr/bin/python3
import time
import sys
import time
import datetime
from socket import socket
import os
import subprocess
import json

def runCmd(cmd):
    proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)
    ret = []
    while True:
        line = proc.stdout.readline().decode('ascii')
        if line is not None and line != '':
            ret.append(line.replace('\n', ''))
        else:
            break
    return ret

#allTZ = {'all': runCmd("/tqdb2026/tools/tzconv -tz"), 'server': 'xx'}
allTZ = {'all': runCmd("timedatectl list-timezones"), 'server': 'xx'}
sys.stdout.write("Content-Type: application/json\r\n")
sys.stdout.write("\r\n")
sys.stdout.write(json.dumps(allTZ))
sys.stdout.flush()
