#!/bin/bash

TEAM=$1
LEAGUE_ID=$(grep league_id squad/"${TEAM}".ini | awk -F= '{print $2}')
TEAM_ID=$(grep team_id squad/"${TEAM}".ini | awk -F= '{print $2}')

for player in $(bash ./src/requests.sh /v1/leagues/"${LEAGUE_ID}"/teams/"${TEAM_ID}"/transferplayers/0 "${ACCESS_TOKEN}" 2>/dev/null | grep '"id"' | jq -c  '.[] | .player | {name, value, price, position}' 2>/dev/null | sed 's/ /_/g')
do
    NAME=$(echo "${player}" | awk -F'"' '{print $4}')
    VALUE=$(echo "${player}" | awk -F'"' '{print $7}' | sed 's/://g' | sed 's/,//g')
    PRICE=$(echo "${player}" | awk -F'"' '{print $9}' | sed 's/://g' | sed 's/,//g')
    POSTITION=$(echo "${player}" | awk -F'"' '{print $11}' | sed 's/:1/A/g' | sed 's/:2/M/g'| sed 's/:3/D/g' | sed 's/:4/G/g')
    echo "$NAME ($POSTITION) : $((PRICE*100/VALUE))"
done | sort -k4 -n -r
