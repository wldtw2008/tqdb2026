#!/bin/bash

source ./profile_tqdb.sh

#mkdir for control TQAlert
mkdir /tmp/TQAlertControl/
chmod 777 /tmp/TQAlertControl/

#for golbal use
echo $CASS_IP":"$CASS_PORT > /tmp/cass.info
echo $D2TQ_IP":"$D2TQ_PORT > /tmp/d2tq.info

#start up demo d2tq server
nohup ./demo_d2tq_server.sh > /tmp/demo_d2tq_server.sh.log &

#start up TQAlert.py
cd $TQDB_DIR/tools ; nohup python3 -u TQAlert.py $CASS_IP $CASS_PORT > /tmp/TQAlert.py.log &

#start up get tick and insert to cassandra
cd $TQDB_DIR/tools && ./autoIns2Cass.sh > /tmp/autoIns2Cass.sh.log &

#start up watchdog of autoIns2Cass
cd $TQDB_DIR/tools && ./watchdogAutoIns2Cass.sh &

