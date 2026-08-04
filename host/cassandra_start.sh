#!/bin/bash

podman run -d --rm \
    --name cassandra \
    -p 9042:9042 \
    -v $(pwd)/../cassandra.data:/var/lib/cassandra:Z \
    cassandra:4.1.11
