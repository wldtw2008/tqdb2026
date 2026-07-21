#!/usr/bin/python3
# coding: utf-8

import time
import sys
import time
import datetime
from socket import socket
from cassandra.cluster import Cluster
import re

szCassIP1="127.0.0.1"
szCassPort=9042
szCMD=""

szCassIP1=sys.argv[1];
szCassPort=sys.argv[2];
szCMD=sys.argv[3];

cluster = Cluster([szCassIP1])
session = cluster.connect()
#session.set_keyspace(szCassDB)
session.execute(szCMD)
