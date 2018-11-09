#!/bin/bash

ACCESS_TOKEN=$1

curl "https://web-api.onlinesoccermanager.com/api/batch?platformId=11&access_token=${ACCESS_TOKEN}" \
    --silent \
    -H 'content-type: text/plain; boundary=o' \
    --data $'--o\r
Content-Type: application/http; msgtype=request\r
\r
GET __REQUEST__ HTTP/1.1\r
Host: web-api.onlinesoccermanager.com/api\r
\r
\r
--o--\r
'
