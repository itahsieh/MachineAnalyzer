import matplotlib.pyplot as plt
import numpy as np

Spec_figsize = (16, 12)
Spec_dpi = 80

def PlotTimeSeries(DataType, data, ImgFile):
    fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
    axes.plot(data)
    axes.set(xlabel='Record number', ylabel = DataType,
           title='Time series of ' + DataType)
    axes.grid()

    fig.savefig(ImgFile)
    print(ImgFile,'generated')
    #plt.show()

def PlotHist(DataType,data, ImgFile):
    # mean of the data
    mu = np.mean(data)
    # standard deviation of distribution
    sigma = np.std(data)

    # number of bins
    num_bins = 50

    fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)

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
    fig.tight_layout()
    
    fig.savefig(ImgFile)
    print(ImgFile,'generated')
    
def PlotSpectrum(DataType, data, ImgFile):
    SamplingRate = 4. * 1024
    DataSize = 4096
    
    dt = 1. / SamplingRate
    nfft = int(DataSize/2)

    assert DataSize <= len(data)
    
    #for i in range(len(data)/DataSize):
    i=0
    dataFFT = data[i*DataSize:(i+1)*DataSize]  

    ## mean of the data
    #mean = np.mean(dataFFT)
    #dataFFT = dataFFT - mean
    
    freqs = np.fft.fftfreq( n=DataSize, d=dt)
    Fourier = np.fft.fft(dataFFT)
    Magnitude = np.abs(Fourier)/nfft
    
    
    print('For the spectrum '+ImgFile)
    
    # energy loss approximation
    EnergyLoss = 0.0
    for i in range(1, nfft):
        EnergyLoss += Magnitude[i]*Magnitude[i] / (freqs[i]*freqs[i]) 
    print('Reduced energy loss = ',EnergyLoss,'μ G^2 s^2')
    
    print('Maximum Magnitude & the corresponding frequencies')
    SortedIndex = np.argsort(Magnitude[1:nfft])
    Nmax = 4
    max_mag_freq_list = []
    for i in range(Nmax):
        idx = -i-1
        SortedIdx = SortedIndex[idx]+1
        frequency = freqs[SortedIdx]
        #if frequency > 0.:
        print( '{:5.3e}'.format(Magnitude[SortedIdx]),
                'mG at',
                freqs[SortedIdx],
                'Hz' 
                )
        max_mag_freq_list.append(frequency)
    
    

    #exit(0)    
    fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
    
    axes.set_title("Magnitude Spectrum", size=24)
    #right_margin = 1.2 * max(max_mag_freq_list)
    right_margin = 300.
    top_margin = 500.
    axes.set_xlim( right = right_margin )
    axes.set_ylim( top = top_margin )
    axes.set_xlabel('Frequency (Hz)', fontsize = 20)
    axes.set_ylabel('Acceleration (mG)', fontsize = 20)
    axes.tick_params(labelsize=16)
    axes.plot( freqs[0:nfft], Magnitude[0:nfft], color='C1')
    
    fig.tight_layout()

    fig.savefig(ImgFile)
    print(ImgFile,'generated')
    #plt.show()
    
    
    
