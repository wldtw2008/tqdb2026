#!/bin/bash

podman run -d \
    --name cassandra \
    -p 9042:9042 \
    -v ../cassandra.data:/var/lib/cassandra:Z \
    cassandra:4.1.11
