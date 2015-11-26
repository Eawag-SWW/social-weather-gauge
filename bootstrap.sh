#!/usr/bin/env bash

ANACONDA_URL=https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda3-2.4.0-Linux-x86_64.sh
ANACONDA_INSTALLER=~/temp/anaconda.sh

mkdir -p ~/temp

if ! [[ -e $ANACONDA_INSTALLER ]]; then
    curl -o $ANACONDA_INSTALLER $ANACONDA_URL
fi

bash $ANACONDA_INSTALLER






