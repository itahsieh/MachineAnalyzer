#!/usr/bin/env python
__author__      = "I-Ta Hsieh"
__copyright__   = "Private use"

# The data path
DataDir = './data/'
DataFile = 'fea1_0409.bin'
#DataFile = 'raw1_1255.bin'
# Data Type: 'feature', 'raw', or 'fft'
DataType = 'feature'

from DataIO import ImportData, FEA_ColumnDict
Array = ImportData( DataType, DataDir+DataFile)

import numpy as np
Array = np.array(Array)

from plot import PlotTimeSiries, PlotHist
VisualType = "Xmean"
PlotTimeSiries( VisualType, data = Array[:,FEA_ColumnDict[VisualType]])
PlotHist( VisualType, data = Array[:,FEA_ColumnDict[VisualType]])

    
