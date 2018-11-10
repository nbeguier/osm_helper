#!/bin/bash

CREDENTIALS=${1:-"credentials"}

TOKEN_TMP_FILE=/tmp/.token
CLIENT_ID=$(grep client_id "${CREDENTIALS}" | awk -F= '{print $2}')
CLIENT_SECRET=$(grep client_secret "${CREDENTIALS}" | awk -F= '{print $2}')
REFRESH_TOKEN=$(grep refresh_token "${CREDENTIALS}" | awk -F= '{print $2}')

curl 'https://web-api.onlinesoccermanager.com/api/token' \
    --data "grant_type=refresh_token&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&refresh_token=${REFRESH_TOKEN}" \
    --silent \
    --output "${TOKEN_TMP_FILE}"

export ACCESS_TOKEN=$(cat "${TOKEN_TMP_FILE}" | jq .access_token | sed 's/"//g')

rm "${TOKEN_TMP_FILE}"
