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
        
        if DataType == 'feature':
            from DataIO import FEA_ColumnDict
            
           
            for VisualType in ['Xmean','Ymean','Zmean','Xstd','Ystd','Zstd']:
                ImageName = filename.split('.')[0]+'_'+VisualType
                PlotTimeSeries( VisualType, 
                        data = Array[:,FEA_ColumnDict[VisualType]], 
                        ImgFile=ImageName+'_Series.png'
                        )
                PlotHist( VisualType, 
                        data = Array[:,FEA_ColumnDict['Xmean']], 
                        ImgFile=ImageName+'_Hist.png'
                        )
            

        
        elif DataType == 'raw':
            VisualType = "Raw Data"
            ImageName = filename.split('.')[0]
            PlotTimeSeries( VisualType, 
                           data = Array, 
                           ImgFile=ImageName+'_Series.png'
                           )
            PlotHist( 
                VisualType, 
                data = Array, 
                ImgFile=ImageName+'_Hist.png'
                )
            
            from FFT import FFTClass
            DataSize = 4096
            SamplingRate = 4. * 1024
            assert DataSize <= len(Array)
    
            #for i in range(len(Array)/DataSize):
            i=0
            dataFFT = Array[i*DataSize:(i+1)*DataSize] 
            
            fft = FFTClass(DataSize, SamplingRate)
            fft.FFT(dataFFT)
            fft.EnergyAnalysis()
            fft.MaxMagnitude()

            PlotSpectrum( 
                fft.freqs, fft.Magnitude,
                ImgFile=ImageName+'_Spec.png'
                )
        
        
   
