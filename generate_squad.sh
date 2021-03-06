#!/bin/bash

echo "Name,Position,Atk,Def,Nationality,Play"

TEAM=$1
LEAGUE_ID=$(grep league_id squad/"${TEAM}".ini | awk -F= '{print $2}')
TEAM_ID=$(grep team_id squad/"${TEAM}".ini | awk -F= '{print $2}')

bash ./src/requests.sh /v1/leagues/"${LEAGUE_ID}"/teams/"${TEAM_ID}"/players 2>/dev/null | grep '"id"' | jq -c  '.[] | . | {name, position, statAtt, statDef, nationality} ' | awk -F '"' '{print $4","$7"POSTE,"$9$11$18",True"}' | sed 's/:4,POSTE/G/g' | sed 's/:3,POSTE/D/g' | sed 's/:2,POSTE/M/g' | sed 's/:1,POSTE/A/g' | sed 's/}//g' | sed 's/://g' | grep -v 'position,null'
