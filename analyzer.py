#!/usr/bin/env python
__author__      = "I-Ta Hsieh"
__copyright__   = "Private use"


# Data IO
DataType, Array = DataImport(DataDir, filename)

def Analyzer(DataType, Array, filename):
    # Plotting
    from plot import *
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
        
        print('For the spectrum of the data '+filename)   
        from FFT import SpecClass
        DataSize = 4096
        SamplingRate = 4.e3
        
        
        assert DataSize <= len(Array)

        #from math import floor
        #for i in range(floor(len(Array)/DataSize)):
        i=0
        dataFFT = Array[i*DataSize:(i+1)*DataSize] 
        
        Spec = SpecClass(SamplingRate)
        Spec.FFT(dataFFT)
        Spec.EnergyAnalysis()
        Spec.MaxMagnitude()

        PlotSpectrum( 
            Spec,
            ImgFile=ImageName+'_Spec.png'
            )
    
    

