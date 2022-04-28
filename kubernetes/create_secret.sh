#!/bin/bash

if [ -z "$1" ] ||  [ -z "$2" ]
then
    echo "Usage: create_secret RELEASE DIR"
    exit 1
fi

RELEASE=$1
DIR=$2

echo "release: $RELEASE"
echo "dir: $DIR"

kubectl create secret tls $RELEASE \
    --key $DIR/tls.key \
    --cert $DIR/tls.crt
    