#!/usr/bin/python3
import time
import sys
import time
import datetime
from socket import socket
import os
import subprocess
import json

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

szSymbol="ALL"

querystrings=os.environ.get("QUERY_STRING", "NA=NA")
mapQS={}
for qs in querystrings.split("&"):
        mapQS[qs.split("=")[0]] = qs.split("=")[1]
if 'symbol' in mapQS: szSymbol = mapQS['symbol']
sys.stdout.write("Content-Type: application/json; charset=UTF-8\r\n")
sys.stdout.write("\r\n")
tmpFile="/tmp/q1min.%d.%d"%(os.getpid(),time.mktime(datetime.datetime.now().timetuple()))
szCMD="./qsym %s %s %s.symbol 0 %s 1 > %s" % (szCassIP1, szCassPort1, szCassDB, szSymbol, tmpFile)
subprocess.call(szCMD, shell=True, cwd=szBinDir) 
fp = open(tmpFile, 'r')
jsonstr=fp.read()
fp.close()
os.remove(tmpFile)
allObjs = json.loads(jsonstr.replace("'",'"'))
sys.stdout.write(json.dumps(allObjs))
sys.stdout.flush()
