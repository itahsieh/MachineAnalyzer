from mpl_toolkits.mplot3d import Axes3D
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
        self.DataName = DataName
        self.VisualOpt = VisualOpt
        self.Array = Array
        if DataType == 'feature':
            self.feaPlot()

        elif DataType == 'raw':
            self.rawPlot()

        if not VisualOpt.SaveFig:
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
        
    def feaPlot(self):
        for VisualType in ['Xmean','Ymean','Zmean','Xstd','Ystd','Zstd']:
            ImageName = self.DataName+'_'+VisualType
            from DataIO import FEA_ColumnDict
            self.PlotTimeSeries( VisualType, 
                    data = self.Array[:,FEA_ColumnDict[VisualType]], 
                    ImgFile=ImageName+'_Series.png'
                    )
            self.PlotHist( VisualType, 
                    data = self.Array[:,FEA_ColumnDict['Xmean']], 
                    ImgFile=ImageName+'_Hist.png'
                    )
            
    def rawPlot(self):
        ImageName = self.DataName
        if self.VisualOpt.series:
            
            VisualType = "Raw Data"
            self.PlotTimeSeries( VisualType, 
                data = self.Array, 
                ImgFile=ImageName+'_Series.png'
                )
            self.PlotHist( 
                VisualType, 
                data = self.Array, 
                ImgFile=ImageName+'_Hist.png'
                )
        
        if self.VisualOpt.spec:
            
            SamplingRate = 4.e3
            from math import floor
            if self.VisualOpt.waterfall:
                DataSize = 4096
                assert DataSize <= len(self.Array)

                
                Ncycle = int(len(self.Array)/DataSize)
                nfft = int(DataSize/2)
                # spectrum cube in the order (Time, Magnitude, frequency)

                spec_mag = np.zeros(( Ncycle, nfft-1))
                for i in range(Ncycle):
                    
                    dataFFT = self.Array[i*DataSize:(i+1)*DataSize] 
                
                    from FFT import SpecClass
                    Spec = SpecClass(SamplingRate)
                    Spec.FFT(dataFFT)
                    
                    if i == 0:
                        spec_freq = Spec.freqs[1:Spec.nfft]
                    spec_mag[i,:] = Spec.Magnitude[1:Spec.nfft]
                    
                print('Done FFT map')
                
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                for i in range(len(spec_freq)):
                    if spec_freq[i] >= 500.:
                        UpperIdx = i
                        break
                
                UpperIdx = int(UpperIdx/2)*2
                half_size = int(UpperIdx/2)                    
                for i in range(UpperIdx):
                    if i < half_size:
                        a = (i + 0.5)/half_size
                        assert 0.0 < a < 1.0
                        b = 1.0 - a
                        cs = [( b, a, 0.0)]
                    else:
                        a = (i + 0.5 - half_size)/half_size
                        assert 0.0 < a < 1.0
                        b = 1.0 - a
                        cs = [( 0.0, b, a)]
                    
                    
                    xs = np.arange(Ncycle)+0.5
                    ys = spec_mag[:,i]
                    ax.bar(xs, 
                           ys, 
                           zs = spec_freq[i], 
                           zdir = 'y', 
                           color=cs, 
                           alpha=0.8)

                ax.set_xlabel('Time')
                ax.set_ylabel('frequency')
                ax.set_zlabel('Magnitude')


            else:
                print('For the spectrum of the data ' + self.DataName)   

                DataSize = 2**floor(np.log(len(self.Array))/np.log(2.))
                
                print(len(self.Array), DataSize)
                dataFFT = self.Array[0:DataSize] 
                
                from FFT import SpecClass
                Spec = SpecClass(SamplingRate)
                Spec.FFT(dataFFT)
                Spec.EnergyAnalysis()
                Spec.MaxMagnitude()

                self.PlotSpectrum( 
                    Spec,
                    ImgFile=ImageName+'_Spec.png'
                    )
    
        
