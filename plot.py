from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

Spec_figsize = (16, 12)
Spec_dpi = 80

class VisualOpt(object):
    def __init__(self, args):
        self.spec = args.spec_view
        self.series = args.series_view
        self.waterfall = args.waterfall_plot
        self.contour = args.contour_plot
        self.scalogram = args.scalogram_plot
        self.SaveFig = not args.show_gui
        self.show_gui = args.show_gui

class Plot():
    def __init__(self, VisualOpt, DataType, DataName, Array):
        self.DataName = DataName
        self.VisualOpt = VisualOpt
        self.Array = Array
        if DataType == 'feature':
            self.PlotFEA()

        elif DataType == 'raw':
            self.PlotRAW()

        if VisualOpt.show_gui:
            plt.show()
        
    def PlotFEA(self):
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
            
    def PlotRAW(self):
        if self.VisualOpt.series:
            self.PlotRAWSeries()
        
        if self.VisualOpt.spec:
            self.PloRAWSpectrum()
            
            if self.VisualOpt.waterfall or self.VisualOpt.contour:
                # FFT map computing
                SamplingRate = 4.e3
                DataSize = 1024
                assert DataSize <= len(self.Array)

                self.Ncycle = int(len(self.Array)/DataSize)
                self.CycleTime = DataSize / SamplingRate
                nfft = int(DataSize/2)
                self.spec_mag = np.zeros(( self.Ncycle, nfft-1))
                for i in range(self.Ncycle):
                    dataFFT = self.Array[i*DataSize:(i+1)*DataSize] 
                
                    from FFT import SpecClass
                    
                    Spec = SpecClass(SamplingRate)
                    Spec.FFT(dataFFT)
                    
                    if i == 0:
                        self.spec_freq = Spec.freqs[1:Spec.nfft]
                    self.spec_mag[i,:] = Spec.Magnitude[1:Spec.nfft]
                print('Done FFT map')
                
                for i in range(len(self.spec_freq)):
                    if self.spec_freq[i] >= 500.:
                        self.UpperFreqIdx = i
                        break
                self.UpperFreqIdx = int(self.UpperFreqIdx/2)*2
                
                if self.VisualOpt.waterfall:
                    self.PlotRAWSpecWaterfall()
                
                if self.VisualOpt.contour:
                    self.PlotRAWSpecContour()
            elif self.VisualOpt.scalogram:
                pass
            
            
                
    def PlotRAWSeries(self): 
        VisualType = "Raw Data"
        self.PlotTimeSeries( VisualType, 
            data = self.Array, 
            ImgFile=self.DataName+'_Series.png'
            )
        self.PlotHist( 
            VisualType, 
            data = self.Array, 
            ImgFile=self.DataName+'_Hist.png'
            )
    
                
    def PlotRAWSpecWaterfall(self):
        fig = plt.figure(figsize=Spec_figsize, dpi=Spec_dpi)
        ax = fig.add_subplot(111, projection='3d')
        half_size = int(self.UpperFreqIdx/2)
        for i in range(self.UpperFreqIdx):
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
            
            xs = ( np.arange(self.Ncycle)+0.5 ) * self.CycleTime
            ys = self.spec_mag[:,i]
            ax.bar( xs,
                    ys, 
                    zs = self.spec_freq[i], 
                    zdir = 'y', 
                    color=cs, 
                    alpha=0.8)

        ax.set_xlabel('Time (second)')
        ax.set_ylabel('frequency (Hz)')
        ax.set_zlabel('Magnitude (mG)')
        
    def PlotRAWSpecContour(self):
        dx = 1.0
        dy = self.spec_freq[1] - self.spec_freq[0]
        x = np.zeros((self.Ncycle, self.UpperFreqIdx))
        y = np.zeros((self.Ncycle, self.UpperFreqIdx))
        for i in range(self.Ncycle):
            for j in range(self.UpperFreqIdx):
                x[i,j] = (i + 0.5) * self.CycleTime
                y[i,j] = self.spec_freq[j]
        z = self.spec_mag[:,0:self.UpperFreqIdx]
        
        from matplotlib.ticker import MaxNLocator
        # x and y are bounds, so z should be the value *inside* those bounds.
        # Therefore, remove the last value from the z array.z = z[:-1, :-1]
        levels = MaxNLocator(nbins=256).tick_values(0., self.spec_mag.max())
        
        # pick the desired colormap, sensible levels, and define a normalization
        # instance which takes data values and translates those into levels.
        from matplotlib.colors import BoundaryNorm
        cmap = plt.get_cmap('inferno')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

        fig, ax = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)

        # contours are *point* based plots, so convert our bound into point
        # centers
        cf = ax.contourf(x, y, z, 
                         levels=levels,
                         cmap=cmap)
        
        cb = fig.colorbar(cf, ax=ax)
        cb.set_label('Magnitude (mG)')
        ax.set_title('Spectrogram')
        ax.set_xlabel('Time (second)')
        ax.set_ylabel('frequency (Hz)')

        # adjust spacing between subplots so `ax1` title and `ax0` tick labels
        # don't overlap
        fig.tight_layout()
        
        if self.VisualOpt.SaveFig:
            self.PlotOutput()

    def PloRAWSpectrum(self):
        print('For the spectrum of the data ' + self.DataName)   

        from math import floor
        DataSize = 2**floor(np.log(len(self.Array))/np.log(2.))
        
        print(len(self.Array), DataSize)
        dataFFT = self.Array[0:DataSize] 
        
        from FFT import SpecClass
        SamplingRate = 4.e3
        Spec = SpecClass(SamplingRate)
        Spec.FFT(dataFFT)
        Spec.EnergyAnalysis()
        Spec.MaxMagnitude()

        self.PlotSpectrum( 
            Spec,
            ImgFile=self.DataName+'_Spec.png'
            )

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
        
        right_margin = 500.
        axes.set_title("Magnitude Spectrum", size=24)

        #right_margin = 1.2 * max(Spec.max_mag_freq_list)
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
        
    def PlotOutput(self):
        self.fig.savefig(self.ImgFile)
        print(self.ImgFile,'generated')
        
