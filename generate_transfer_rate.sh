#!/bin/bash

TRANSFER_BATCH=$1

for player in $(bash $1 | jq -c  '.[] | .player | {name, value, price, position}' 2>/dev/null | sed 's/ /_/g'); do NAME=$(echo $player | awk -F'"' '{print $4}'); VALUE=$(echo $player | awk -F'"' '{print $7}' | sed 's/://g' | sed 's/,//g'); PRICE=$(echo $player | awk -F'"' '{print $9}' | sed 's/://g' | sed 's/,//g'); POSTITION=$(echo $player | awk -F'"' '{print $11}'); echo "$NAME ($POSTITION) : $((PRICE*100/VALUE))"; done | sort -k4 -n

