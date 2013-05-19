#!/bin/bash

. common.sh

ID=`uuidgen`
FILE=/tmp/zoe-mail-$ID
BODY=`cat | base64`
echo $BODY

MSG="dst=mail&tag=received&body=$BODY"

send "$MSG"