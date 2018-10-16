echo "Name,Position,Atk,Def,Nationality,Play"
bash batch/get_${1}.sh | jq -c  '.[] | . | {name, position, statAtt, statDef, nationality} ' | awk -F '"' '{print $4","$7"POSTE,"$9$11$18",True"}' | sed 's/:4,POSTE/G/g' | sed 's/:3,POSTE/D/g' | sed 's/:2,POSTE/M/g' | sed 's/:1,POSTE/A/g' | sed 's/}//g' | sed 's/://g' | grep -v 'position,null'
