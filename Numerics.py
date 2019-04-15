import matplotlib.pyplot as plt
import numpy as np

Spec_figsize = (16, 12)
Spec_dpi = 80

def BiasEstimate(array):
    
    pass






def FFTExam():
    ImageFileName = "FFTExam.png"
    
    SamplingRate = 1.e3
    DataSize = 4096
    dt = 1./SamplingRate
    nfft = int(DataSize/2)
    
    freqs = np.fft.fftfreq( n=DataSize, d=dt)
    
    A1 = 24.; f1 = 250.; phi1 =  23./360.*2.*np.pi
    A2 = 5.5; f2 = 60. ; phi2 = 345./360.*2.*np.pi
    omega1 = 2. * np.pi * f1
    omega2 = 2. * np.pi * f2
    data = np.zeros(DataSize)
    for i in range(DataSize):
        data[i] = A1 * np.sin(omega1*i*dt+phi1) + A2 * np.sin(omega2*i*dt+phi2) 

    
    Fourier = np.fft.fft(data)
    Magnitude = np.abs(Fourier)/nfft

    SortedIndex = np.argsort(Magnitude[1:nfft])
    Nmax = 10
    max_mag_freq_list = []
    print('Maximum Magnitude in the spectrum '+ImageFileName)
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
    axes.set_title("Magnitude Spectrum")
    
    axes.plot( freqs[0:nfft], Magnitude[0:nfft], color='C1')
    
    fig.tight_layout()
    
    
    fig.savefig(ImageFileName)
    
FFTExam()
