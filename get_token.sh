#!/bin/bash

CREDENTIALS=$1

CLIENT_ID=$(grep client_id "${CREDENTIALS}" | awk -F= '{print $2}')
CLIENT_SECRET=$(grep client_secret "${CREDENTIALS}" | awk -F= '{print $2}')
REFRESH_TOKEN=$(grep refresh_token "${CREDENTIALS}" | awk -F= '{print $2}')

curl 'https://web-api.onlinesoccermanager.com/api/token' \
    --data "grant_type=refresh_token&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&refresh_token=${REFRESH_TOKEN}" \
    -s
