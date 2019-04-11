#!/usr/bin/env python
__author__      = "I-Ta Hsieh"
__copyright__   = "Private use"

# The data path
DataDir = './data/'

# DataFile: name of data 
# DataType: 'feature', 'raw', or 'fft'

#DataFile = 'fea1_0409.bin'
DataFile = 'raw1_1255.bin'




# Data IO
from DataIO import ImportFeaData, ImportRawData, FEA_ColumnDict

DataPath = DataDir+DataFile
try:
    fh = open(DataPath, 'r')
    fh.close()
except FileNotFoundError:
    print('Data not found:',DataPath)
    exit(1)


if 'fea' in DataFile:
    DataType = 'feature'
elif 'raw' in DataFile:
    DataType = 'raw'
elif 'fft' in DataFile:
    DataType = 'fft' 
else:
    print('Could not identify the data type')
    exit(1)

if DataType == 'feature':
    Array = ImportFeaData(DataPath)
elif DataType == 'raw':
    Array = ImportRawData(DataPath)
elif DataType == 'fft':
    pass

import numpy as np
Array = np.array(Array)

#exit(0)

# Plotting
from plot import PlotTimeSiries, PlotHist, PlotSpectrum
if DataType == 'feature':
    VisualType = "Xmean"
    PlotTimeSiries( VisualType, data = Array[:,FEA_ColumnDict[VisualType]])
    PlotHist( VisualType, data = Array[:,FEA_ColumnDict[VisualType]])
elif DataType == 'raw':
    VisualType = "Raw Data"
    #PlotTimeSiries( VisualType, data = Array)data
    #PlotHist( VisualType, data = Array)
    PlotSpectrum( VisualType, data = Array)
   
   
   
