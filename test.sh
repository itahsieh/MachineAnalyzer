#!/bin/bash

CASE=${1} 
case $CASE in
    "scalogram")
        ./viewer.py -i data/fan_20190422/DAC_raw_0422_abnor_high.bin \
        --show \
        --spec \
        --scalogram
        ;;
    "waterfall")
        ./viewer.py -i data/fan_20190409/raw3_1255.bin \
        --show \
        --spec \
        --waterfall
        ;;
    "contour")
        ./viewer.py -i data/fan_20190409/raw3_1255.bin \
        --show \
        --spec \
        --contour
        ;;
    "spec")
        ./viewer.py -i data/shaking_table_20199223/0223_300_zraw3.bin \
        --show \
        --spec
        ;;
    "series")
        ./viewer.py -i data/shaking_table_20199223/0223_300_zraw3.bin \
        --show \
        --series
        ;;
    "fea")
        ./viewer.py -i data/fan_20190409/fea3_0409.bin \
        --show \
        --series
        ;;
    *)
        exit 1
        ;;
esac
