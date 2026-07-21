#!/usr/bin/python3
import time
import sys
import time
import datetime
from socket import socket
import os
import subprocess

szBinDir='/tqdb2026/tools/'
szCassIP1="127.0.0.1"
szCassPort1="7496"
szCassDB="tqdb1"
try:
    f = open('/tmp/cass.info', 'r')
    line = f.read().strip()
    szCassIP1 = line.split(':')[0]
    szCassPort1 = line.split(':')[1]
    f.close()
except:
    pass

querystrings=os.environ.get("QUERY_STRING", "NA=NA")
mapQS={}
for qs in querystrings.split("&"):
        mapQS[qs.split("=")[0]] = qs.split("=")[1]

sys.stdout.write("Content-Type: text/plain\r\n")
sys.stdout.write("\r\n")
tmpFile="/tmp/q1min.%d.%d"%(os.getpid(),time.mktime(datetime.datetime.now().timetuple()))
szCMD="./qsym %s %s %s.symbol 0 ALL 1 > %s" % (szCassIP1, szCassPort1, szCassDB, tmpFile)
subprocess.call(szCMD, shell=True, cwd=szBinDir) 
fp = open(tmpFile, 'rb')
sys.stdout.write(fp.read())
sys.stdout.flush()
os.remove(tmpFile)
