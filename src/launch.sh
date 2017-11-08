#!/bin/bash
psql -U ubuntu -d ubuntu -a -f bdd/distributed_create.sql
python python/client.py &