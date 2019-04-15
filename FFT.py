import numpy as np



class FFTClass():
    def __init__(self, DataSize, SamplingRate):
        self.DataSize = DataSize
        self.SamplingRate = SamplingRate
        
        

    def FFT( self, dataFFT, SamplingRate):
        DataSize = len(dataFFT)
        
        dt = 1. / SamplingRate
        nfft = int(DataSize/2)
        freqs = np.fft.fftfreq( n=DataSize, d=dt)
        Fourier = np.fft.fft(dataFFT)
        Magnitude = np.abs(Fourier)/nfft


    def EnergyAnalysis(self):
        # energy loss approximation
        EnergyLoss = 0.0
        for i in range(1, nfft):
            EnergyLoss += Magnitude[i]*Magnitude[i] / (freqs[i]*freqs[i]) 
        print('Reduced energy loss = ',EnergyLoss,'μ G^2 s^2')
        
        return EnergyLoss
    
    def MaxMagnitude(self):    
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
