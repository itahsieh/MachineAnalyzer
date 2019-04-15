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
    
def PlotSpectrum( Spec, ImgFile):  
    fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
    
    
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
    
    fig.tight_layout()

    fig.savefig(ImgFile)
    print(ImgFile,'generated')
    #plt.show()
    
    
    
