#!/bin/bash

REQUEST=$1
ACCESS_KEY=$2

sed "s#__REQUEST__#${REQUEST}#g" ./src/batch_template.sh | bash -s "${ACCESS_KEY}"
