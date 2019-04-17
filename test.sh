#!/bin/bash

CASE=${1} 
case $CASE in
    "view")
        pwd
        ./viewer.py -i data/raw/0223_300_zraw3.bin --show --spec
        ;;
    *)
        exit 1
        ;;
esac
