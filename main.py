#!/usr/bin/env python3
__author__      = "I-Ta Hsieh"
__copyright__   = "Private use"

# The data path
#DataDir = './data/'
DataDir = './data/raw/'

# DataFile: name of data
# Attention: raw dat must contain 'raw' in file name
#            feature data must contain 'fea' in file name
#DataFile = ['fea1_0409.bin']

#DataFile = [
    #'raw1_1255.bin',
    #'raw2_1255.bin',
    #'raw3_1255.bin'
    #]

#DataFile = ['raw3_1255.bin']

DataFile = ['0223_200_zraw3.bin']


from analyzer import Analyzer
for filename in DataFile:
    # Data IO
    DataType, Array = DataImport(DataDir, filename)
    # Call Analyzer
    Analyzer( DataType, Array, filename)


