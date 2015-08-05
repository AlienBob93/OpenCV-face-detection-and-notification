#!/bin/bash

API='INSERT PUSHBULLET API KEY HERE'
MSG="$1"

curl -u $API: https://api.pushbullet.com/v2/pushes -d type=note -d title="Alert" -d body="$MSG"
