import matplotlib.pyplot as plt
import numpy as np

Spec_figsize = (16, 12)
Spec_dpi = 80

def PlotTimeSiries(DataType, data):
    fig, ax = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
    ax.plot(data)
    ax.set(xlabel='Record number', ylabel = DataType,
           title='Time series of ' + DataType)
    ax.grid()

    ImageFileName = "figure1.png"
    fig.savefig(ImageFileName)
    #plt.show()

def PlotHist(DataType,data):
    # mean of the data
    mu = np.mean(data)
    # standard deviation of distribution
    sigma = np.std(data)

    # number of bins
    num_bins = 50

    fig, ax = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)

    # the histogram of the data
    n, bins, patches = ax.hist(data, num_bins, density=1)

    # add a 'best fit' line
    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
        np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    ax.plot(bins, y, '--')
    ax.set_xlabel(DataType)
    ax.set_ylabel('Probability density')
    ax.set_title(r'Histogram of ' + DataType
                 +': $\mu=' + '{:f}'.format(mu)
                 +'$, $\sigma=' + '{:f}'.format(sigma)+'$')

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    
    ImageFileName = "figure2.png"
    fig.savefig(ImageFileName)
    #plt.show()
    
def PlotSpectrum(DataType,data):
    DataSize = 4096
    dt = 1./1e-3
    nfft = int(DataSize/2)
    
    freqs = np.fft.fftfreq( n=DataSize, d=dt)
    data = data[0:DataSize]  

    # mean of the data
    mean = np.mean(data)
    data = data - mean
    
    Fourier = np.fft.fft(data)
    Magnitude = np.abs(Fourier)
    
    idx = np.argsort(freqs)

    #exit(0)    
    fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
    axes.set_title("Magnitude Spectrum")
    
    axes.semilogy( freqs[0:nfft], Magnitude[0:nfft], color='C1')
    
    fig.tight_layout()
    
    ImageFileName = "figure3.png"
    fig.savefig(ImageFileName)
    #plt.show()
    
    
    
