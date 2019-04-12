#!/usr/bin/env python
__author__      = "I-Ta Hsieh"
__copyright__   = "Private use"

# The data path
DataDir = './data/'

# DataFile: name of data 
#DataFile = 'fea1_0409.bin'
DataFile = [
    'raw1_1255.bin',
    'raw2_1255.bin',
    'raw3_1255.bin'
    ]

from analyzer import Analyzer
Analyzer( DataDir, DataFile)


