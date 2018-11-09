# osm-helper

# LineUp

```
# Create your team identifier
cp squad/team.ini.example squad/team.ini
vim squad/team.ini
```

```
# Generate your team squad
./generate_squad.sh team > squad/team.csv

cat squad/team.csv
```

```
# Check your possible lineup
./osm_lineup.py squad/team.csv
```

## Login

```
# Create credentials file
cp credentials.example credentials
vim credentials
```

```
# Generate a token
./get_token.sh [credentials file]

export ACCESS_KEY=XXXXXX
```

## Transfer

```
# Check the transfer list of your league
./generate_transfer_rate.sh team ${ACCESS_KEY}
```
