#!/bin/bash

CASE=${1} 
case $CASE in
    "waterfall")
        ./viewer.py -i data/raw/0223_300_zraw3.bin --show --spec --waterfall
        ;;
    "spec")
        ./viewer.py -i data/raw/0223_300_zraw3.bin --show --spec
        ;;
    "series")
        ./viewer.py -i data/raw/0223_300_zraw3.bin --show --series
        ;;
    "fea")
        ./viewer.py -i data/fea3_0409.bin --show --series
        ;;
    *)
        exit 1
        ;;
esac
