#!/usr/bin/env python
__author__      = "I-Ta Hsieh"
__copyright__   = "Private use"

from plot import *

def Analyzer(DataDir, DataFile):
    # Data IO
    for filename in DataFile:
        DataPath = DataDir+filename
        # try if the file exists
        try:
            fh = open(DataPath, 'r')
            fh.close()
        except FileNotFoundError:
            print('Data not found:',DataPath)
            exit(1)

        # DataType: 'feature', 'raw', or 'fft'
        if 'fea' in filename:
            DataType = 'feature'
            from DataIO import ImportFeaData
            Array = ImportFeaData(DataPath)
        elif 'raw' in filename:
            DataType = 'raw'
            from DataIO import ImportRawData
            Array = ImportRawData(DataPath)
        elif 'fft' in filename:
            DataType = 'fft' 
            pass
        else:
            print('Could not identify the data type')
            exit(1)
        
        # convert the array to numpy type
        import numpy as np
        Array = np.array(Array)

        #exit(0)

        # Plotting
        ImageName = filename.split('.')[0]+'.png'
        if DataType == 'feature':
            VisualType = "Xmean"
            from DataIO import FEA_ColumnDict

            PlotTimeSeries( VisualType, 
                           data = Array[:,FEA_ColumnDict[VisualType]], 
                           ImgFile='Series_'+ImageName
                           )
            PlotHist( VisualType, 
                     data = Array[:,FEA_ColumnDict[VisualType]], 
                           ImgFile='Hist_'+ImageName
                     )
        
        elif DataType == 'raw':
            VisualType = "Raw Data"
            PlotTimeSeries( VisualType, 
                           data = Array, 
                           ImgFile='Series_'+ImageName
                           )
            PlotHist( 
                VisualType, 
                data = Array, 
                ImgFile='Hist_'+ImageName
                )
            PlotSpectrum( 
                VisualType, 
                data = Array,
                ImgFile='Spec_'+ImageName
                )
        
        
   
