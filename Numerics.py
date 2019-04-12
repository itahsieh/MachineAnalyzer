import matplotlib.pyplot as plt
import numpy as np

Spec_figsize = (16, 12)
Spec_dpi = 80

def BiasEstimate(array):
    
    pass


def FFTExam():
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
    Magnitude = np.abs(Fourier)

    #exit(0)    
    fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
    axes.set_title("Magnitude Spectrum")
    
    axes.plot( freqs[0:nfft], Magnitude[0:nfft], color='C1')
    
    fig.tight_layout()
    
    ImageFileName = "figure3.png"
    fig.savefig(ImageFileName)
    
FFTExam()
