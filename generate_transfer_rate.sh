#!/bin/bash

TRANSFER_BATCH=$1

for player in $(bash "${TRANSFER_BATCH}" 2>/dev/null | grep '"id"' | jq -c  '.[] | .player | {name, value, price, position}' 2>/dev/null | sed 's/ /_/g')
do
    NAME=$(echo "${player}" | awk -F'"' '{print $4}')
    VALUE=$(echo "${player}" | awk -F'"' '{print $7}' | sed 's/://g' | sed 's/,//g')
    PRICE=$(echo "${player}" | awk -F'"' '{print $9}' | sed 's/://g' | sed 's/,//g')
    POSTITION=$(echo "${player}" | awk -F'"' '{print $11}' | sed 's/:1/A/g' | sed 's/:2/M/g'| sed 's/:3/D/g' | sed 's/:4/G/g')
    echo "$NAME ($POSTITION) : $((PRICE*100/VALUE))"
done | sort -k4 -n -r
