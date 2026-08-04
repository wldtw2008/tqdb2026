#!/bin/bash

echo Set crontab file mode to 644
chmod 644 ../tqdb2026.files/etc/crontab


podman run -d --rm --name tqdb2026  \
	--hostname TQDB2026 \
	--security-opt=label=disable \
	-p 8080:80 \
	-v $(pwd)/../tqdb2026.files/tqdb2026:/tqdb2026 \
	-v $(pwd)/../tqdb2026.oldtick/:/tqdb2026/oldtick \
	-v $(pwd)/../tqdb2026.files/etc/crontab:/etc/crontab \
	-v $(pwd)/../tqdb2026.files/etc/TQDB.vhost.conf:/etc/httpd/conf.d/TQDB.vhost.conf \
	-v $(pwd)/../tqdb2026.files/www:/var/www \
	tqdb2026:rhel8 
