#!/bin/bash

podman run -d --rm --name tqdb2026  \
	--hostname TQDB2026 \
	--security-opt=label=disable \
	-p 8080:80 \
	-v ../tqdb2026.files/tqdb2026:/tqdb2026 \
	-v ../tqdb2026.oldtick/:/tqdb2026/oldtick \
	-v ../tqdb2026.files/etc/crontab:/etc/crontab \
	-v ../tqdb2026.files/etc/TQDB.vhost.conf:/etc/httpd/conf.d/TQDB.vhost.conf \
	-v ../tqdb2026.files/www:/var/www \
	tqdb2026:rhel8 
