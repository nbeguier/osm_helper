#!/bin/bash

CREDENTIALS=${1:-"credentials"}

TOKEN_TMP_FILE=/tmp/.token
CLIENT_ID=$(grep client_id "${CREDENTIALS}" | awk -F= '{print $2}')
CLIENT_SECRET=$(grep client_secret "${CREDENTIALS}" | awk -F= '{print $2}')
USERNAME=$(grep username "${CREDENTIALS}" | awk -F= '{print $2}')
PASSWORD=$(grep password "${CREDENTIALS}" | awk -F= '{print $2}')

curl 'https://web-api.onlinesoccermanager.com/api/token' \
    --data "grant_type=password&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&password=${PASSWORD}&userName=${USERNAME}" \
    --silent \
    --output "${TOKEN_TMP_FILE}"

export ACCESS_TOKEN=$(cat "${TOKEN_TMP_FILE}" | jq .access_token | sed 's/"//g')

rm "${TOKEN_TMP_FILE}"
