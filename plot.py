from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

Spec_figsize = (16, 12)
Spec_dpi = 80



class Plot():
    def __init__(self, VisualOpt, Array):
        self.DataName = VisualOpt.filename.split('.')[0]
        self.VisualOpt = VisualOpt
        self.SamplingRate = VisualOpt.sampling
        self.Array = Array
        if VisualOpt.DataType == 'feature':
            self.PlotFEA()

        elif VisualOpt.DataType == 'raw':
            self.PlotRAW()

        if VisualOpt.show_gui:
            plt.show()
        
    def PlotFEA(self):
        for VisualType in ['Xmean',
                           'Ymean',
                           'Zmean',
                           'Xstd',
                           'Ystd',
                           'Zstd',
                           'Xkurtosis',
                           'Ykurtosis',
                           'Zkurtosis']:
            ImageName = self.DataName+'_'+VisualType
            from DataIO import FEA_ColumnDict
            self.PlotTimeSeries( VisualType, 
                    data = self.Array[:,FEA_ColumnDict[VisualType]], 
                    ImgFile=ImageName+'_Series.png'
                    )
            
            if self.VisualOpt.record_range != None:
                HistData = self.Array[
                    self.VisualOpt.record_range[0]:self.VisualOpt.record_range[1],
                    FEA_ColumnDict[VisualType]
                    ]
            else:
                HistData = self.Array[:, FEA_ColumnDict[VisualType]]
            self.PlotHist( VisualType, 
                    data = HistData, 
                    ImgFile=ImageName+'_Hist.png'
                    )
            
    def PlotRAW(self):
        PlotType = self.VisualOpt.PlotType
        if 'series' in PlotType:
            self.PlotRAWSeries()
        
        if 'spec' in PlotType:
            self.PloRAWSpectrum()
            
        if 'waterfall' in PlotType or 'contour' in PlotType or 'velocity' in PlotType:
            # FFT map computing
            if self.VisualOpt.record_range != None:
                self.Array = self.Array[
                    self.VisualOpt.record_range[0]:
                        self.VisualOpt.record_range[1]+1
                    ]
            
            DataSize = 1024
            assert DataSize <= len(self.Array)

            self.Ncycle = int(len(self.Array)/DataSize)
            self.CycleTime = DataSize / self.SamplingRate
            nfft = int(DataSize/2)
            self.spec_mag = np.zeros(( self.Ncycle, nfft-1))
            
            bias = self.VisualOpt.bias
            self.acc_dc = np.zeros(self.Ncycle)
            self.acc_total = np.zeros(self.Ncycle)
            for i in range(self.Ncycle):
                dataFFT = self.Array[i*DataSize:(i+1)*DataSize] - bias
            
                from FFT import SpecClass
                
                Spec = SpecClass(self.SamplingRate)
                Spec.FFT(dataFFT)
                
                if i == 0:
                    self.spec_freq = Spec.freqs[1:Spec.nfft]
                self.spec_mag[i,:] = Spec.Magnitude[1:Spec.nfft]
                
                self.acc_dc[i] = Spec.Fourier[0].real / Spec.DataSize # mG
                self.acc_total[i] = Spec.Fourier[0].real * 9.8 * 1e-3 / self.SamplingRate # delta m/s
            
            print('Done FFT map')
            
            for i in range(len(self.spec_freq)):
                if self.spec_freq[i] >= 0.25 * self.SamplingRate:
                    self.UpperFreqIdx = i
                    break
            self.UpperFreqIdx = int(self.UpperFreqIdx/2)*2
            
            if self.VisualOpt.record_range != None:
                self.start_time = self.VisualOpt.record_range[0] / self.SamplingRate
            else:
                self.start_time = 0.0
            
            if 'waterfall' in PlotType:
                self.PlotRAWSpecWaterfall()
            
            if 'contour' in PlotType:
                self.PlotRAWSpecContour()
                
            if 'velocity' in PlotType:
                self.PlotRAWVelocity()
        
        elif 'scalogram' in PlotType:
            from scipy import signal
            MaxWidth = 31
            widths = np.arange(1, MaxWidth)
            cwtmatr = signal.cwt(self.Array, signal.ricker, widths)


            fig, ax = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
            
            imshow = ax.imshow(cwtmatr, 
                        extent=[0.0, len(self.Array)/self.SamplingRate, 1, MaxWidth], 
                        cmap='seismic',
                        aspect='auto',
                        vmax=abs(cwtmatr).max(), 
                        vmin=-abs(cwtmatr).max() )
            
            cb = fig.colorbar(imshow, ax=ax)
            cb.set_label('percentage')
            ax.set_title('Scalogram')
            ax.set_xlabel('Time (second)')
            ax.set_ylabel('scales a')
        
                
    def PlotRAWSeries(self):
        if self.VisualOpt._3ax_raw_data:            
            
            if self.VisualOpt.axis == 'x':
                self.PlotTimeSeries( "Acceleration along X-axis", 
                    data = self.Array, 
                    ImgFile=self.DataName+'_X-axis_Series.png'
                    )
            elif self.VisualOpt.axis == 'y':
                self.PlotTimeSeries( "Acceleration along Y-axis", 
                    data = self.Array, 
                    ImgFile=self.DataName+'_Y-axis_Series.png'
                    )
            elif self.VisualOpt.axis == 'z':
                self.PlotTimeSeries( "Acceleration along Z-axis", 
                    data = self.Array, 
                    ImgFile=self.DataName+'_Z-axis_Series.png'
                    )
            else:
                self.PlotTimeSeries( "Acceleration along X-axis", 
                    data = self.Array[0,:], 
                    ImgFile=self.DataName+'_X-axis_Series.png'
                    )
                self.PlotTimeSeries( "Acceleration along Y-axis", 
                    data = self.Array[1,:], 
                    ImgFile=self.DataName+'_Y-axis_Series.png'
                    )
                self.PlotTimeSeries( "Acceleration along Z-axis", 
                    data = self.Array[2,:], 
                    ImgFile=self.DataName+'_Z-axis_Series.png'
                    )
        else:
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
            
            xs = ( np.arange(self.Ncycle)+0.5 ) * self.CycleTime + self.start_time
            ys = self.spec_mag[:,i]
            ax.bar( xs,
                    ys, 
                    zs = self.spec_freq[i], 
                    zdir = 'y', 
                    color=cs, 
                    alpha=0.8)

        ax.set_xlabel('Time (second)')
        ax.set_ylabel('frequency (Hz)')
        ax.set_zlabel
        
        if self.VisualOpt.SaveFig:
            self.PlotOutput()
        
    def PlotRAWSpecContour(self):
        x = np.zeros((self.Ncycle, self.UpperFreqIdx))
        y = np.zeros((self.Ncycle, self.UpperFreqIdx))
        for i in range(self.Ncycle):
            for j in range(self.UpperFreqIdx):
                x[i,j] = (i + 0.5) * self.CycleTime + self.start_time
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

        self.fig, ax = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)

        # contours are *point* based plots, so convert our bound into point
        # centers
        contourf = ax.contourf(x, y, z, 
                         levels=levels,
                         cmap=cmap)
        
        cb = self.fig.colorbar(contourf, ax=ax)
        cb.set_label('Magnitude (mG)')
        ax.set_title('Spectrogram')
        ax.set_xlabel('Time (second)')
        ax.set_ylabel('frequency (Hz)')

        # adjust spacing between subplots so `ax1` title and `ax0` tick labels
        # don't overlap
        self.fig.tight_layout()
        
        self.ImgFile = self.DataName+'_contour.png'
        
        if self.VisualOpt.SaveFig:
            self.PlotOutput()

    def PlotRAWVelocity(self):
        threshold = self.VisualOpt.threshold
        x = np.zeros(self.Ncycle+1)
        v = np.zeros(self.Ncycle+1)
        x[0] = self.start_time
        v[0] = self.VisualOpt.IV # m/s
        for i in range(self.Ncycle):
            x[i+1] = x[i] + self.CycleTime 
            if np.abs(self.acc_dc[i]) >= threshold:
                v[i+1] = v[i] + self.acc_total[i] # m/s
            else:
                v[i+1] =v[i]
                
        print('Maximum velocity: ',np.max(v),'m/s')
        print('Minimum velocity: ',np.min(v),'m/s')
        
        self.fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
        
        axes.set_title("Velocity", size=24)
        axes.set_xlabel('Time (second)', fontsize = 20)
        axes.set_ylabel('Velocity (km/hr)', fontsize = 20)
        axes.tick_params(labelsize=16)
        axes.plot( x, v*3.6, color='C0')

        # adjust spacing between subplots so `ax1` title and `ax0` tick labels
        # don't overlap
        self.fig.tight_layout()
        
        self.ImgFile = self.DataName+'_velocity.png'
        
        if self.VisualOpt.SaveFig:
            self.PlotOutput()


    def PloRAWSpectrum(self):
        print('For the spectrum of the data ' + self.DataName)   

        from math import floor
        if self.VisualOpt.record_range == None:
            DataSize = 2**floor(np.log(len(self.Array))/np.log(2.))
            dataFFT = self.Array
            print('Thea data size:',DataSize)
            filename = self.DataName+'_Spec.png'
        else:
            dataFFT = self.Array[
                self.VisualOpt.record_range[0]:
                    self.VisualOpt.record_range[1]+1
                ]
            print('The data range (number of record):',self.VisualOpt.record_range)
            filename = self.DataName + '_range' + str(self.VisualOpt.record_range[0]) + '_' + str(self.VisualOpt.record_range[1]) + '_Spec.png'
        
        from FFT import SpecClass
        Spec = SpecClass(self.SamplingRate)
        Spec.FFT(dataFFT)
        Spec.EnergyAnalysis()
        Spec.MaxMagnitude()
        
        mean_acceleration   = Spec.Fourier[0].real/Spec.DataSize     # mG
        total_acceleration  = Spec.Fourier[0].real * 9.8 * 1e-3 / self.SamplingRate # m/s
        print('The sampling rate is ','{:10.4f}'.format(self.SamplingRate),'Hz')
        print('Mean value at FFT 0Hz:')
        print('{:10.4f}'.format(mean_acceleration),'mG')
        print('Total Acceleration:')
        print('{:10.4f}'.format(total_acceleration*3.6),'km/hr')
        

        self.PlotSpectrum( Spec, ImgFile=self.DataName+'_Spec.png')


    def PlotTimeSeries(self, DataType, data, ImgFile):
        self.ImgFile = ImgFile
        
        self.fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
        axes.plot(data)
        axes.set(xlabel='Record number', ylabel = DataType,
            title='Time series of ' + DataType)

        axes.grid(True)
        if self.VisualOpt.record_range != None:
            axes.set_xlim( left  = self.VisualOpt.record_range[0],
                           right = self.VisualOpt.record_range[1])
        
        
        if self.VisualOpt.SaveFig:
            self.PlotOutput()
        
    def PlotHist( self, DataType, data, ImgFile):
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
        
