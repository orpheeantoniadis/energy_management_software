#!/bin/bash
scp -r -i macbookpro.pem -P 10196 ../bdd ubuntu@hepiacloud.hesge.ch:.
scp -r -i macbookpro.pem -P 10196 ../python ubuntu@hepiacloud.hesge.ch:.
scp -r -i macbookpro.pem -P 10196 launch.sh ubuntu@hepiacloud.hesge.ch:.
./connect.sh