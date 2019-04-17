import matplotlib.pyplot as plt
import numpy as np

class VisualOpt(object):
    def __init__(self, args):
        self.spec = args.spec_view
        self.series = args.series_view
        self.waterfall = args.waterfall_plot
        self.SaveFig = not args.show_gui


Spec_figsize = (16, 12)
Spec_dpi = 80




class PlotClass():
    def __init__(self, VisualOpt, DataType, DataName, Array):
        self.VisualOpt = VisualOpt
        if DataType == 'feature':
            for VisualType in ['Xmean','Ymean','Zmean','Xstd','Ystd','Zstd']:
                ImageName = DataName+'_'+VisualType
                from DataIO import FEA_ColumnDict
                self.PlotTimeSeries( VisualType, 
                        data = Array[:,FEA_ColumnDict[VisualType]], 
                        ImgFile=ImageName+'_Series.png'
                        )
                self.PlotHist( VisualType, 
                        data = Array[:,FEA_ColumnDict['Xmean']], 
                        ImgFile=ImageName+'_Hist.png'
                        )
            

        elif DataType == 'raw':
            ImageName = DataName
            if VisualOpt.series:
                VisualType = "Raw Data"
                self.PlotTimeSeries( VisualType, 
                                data = Array, 
                                ImgFile=ImageName+'_Series.png'
                                )
                self.PlotHist( 
                    VisualType, 
                    data = Array, 
                    ImgFile=ImageName+'_Hist.png'
                    )
            
            if VisualOpt.spec:
                print('For the spectrum of the data ' + DataName)   
                
                DataSize = 4096
                SamplingRate = 4.e3
                assert DataSize <= len(Array)

                #from math import floor
                #for i in range(floor(len(Array)/DataSize)):
                i=0
                dataFFT = Array[i*DataSize:(i+1)*DataSize] 
                
                from FFT import SpecClass
                Spec = SpecClass(SamplingRate)
                Spec.FFT(dataFFT)
                Spec.EnergyAnalysis()
                Spec.MaxMagnitude()

                self.PlotSpectrum( 
                    Spec,
                    ImgFile=ImageName+'_Spec.png'
                    )

        if not VisualOpt.SaveFig:
            import matplotlib.pyplot as plt
            plt.show()
        
        
    def PlotOutput(self):
        self.fig.savefig(self.ImgFile)
        print(self.ImgFile,'generated')

    def PlotTimeSeries(self, DataType, data, ImgFile):
        self.ImgFile = ImgFile
        
        self.fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
        axes.plot(data)
        axes.set(xlabel='Record number', ylabel = DataType,
            title='Time series of ' + DataType)
        axes.grid()
        
        if self.VisualOpt.SaveFig:
            self.PlotOutput()
        
    def PlotHist( self, DataType,data, ImgFile):
        self.ImgFile = ImgFile
        
        # mean of the data
        mu = np.mean(data)
        # standard deviation of distribution
        sigma = np.std(data)

        # number of bins
        num_bins = 50

        self.fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)

        # the histogram of the data
        n, bins, patches = axes.hist(data, num_bins, density=1)

        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
            np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        axes.plot(bins, y, '--', linewidth=4.0)
        axes.set_xlabel(DataType)
        axes.set_ylabel('Probability density')
        axes.set_title(r'Histogram of ' + DataType
                    +': $\mu=' + '{:f}'.format(mu)
                    +'$, $\sigma=' + '{:f}'.format(sigma)+'$')

        # Tweak spacing to prevent clipping of ylabel
        self.fig.tight_layout()
        
        if self.VisualOpt.SaveFig:
            self.PlotOutput()
        
    def PlotSpectrum( self, Spec, ImgFile):
        self.ImgFile = ImgFile
        
        self.fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
        
        #right_margin = 300.
        axes.set_title("Magnitude Spectrum", size=24)
        right_margin = 1.2 * max(Spec.max_mag_freq_list)
        MaxIdx = Spec.SortedIndex[-1]+1
        top_margin = 1.2 * Spec.Magnitude[MaxIdx]
        axes.set_xlim( right = right_margin )
        axes.set_ylim( top = top_margin )
        axes.set_xlabel('Frequency (Hz)', fontsize = 20)
        axes.set_ylabel('Acceleration (mG)', fontsize = 20)
        
        axes.tick_params(labelsize=16)
        axes.plot( Spec.freqs[0:Spec.nfft], Spec.Magnitude[0:Spec.nfft], color='C1')
        
        self.fig.tight_layout()

        if self.VisualOpt.SaveFig:
            self.PlotOutput()
        
    
        
        
        
