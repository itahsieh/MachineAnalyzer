import numpy as np

class SpecClass():
    def __init__(self, SamplingRate):
        self.SamplingRate = SamplingRate

    def FFT( self, dataFFT):
        dt = 1. / self.SamplingRate
        self.DataSize = len(dataFFT)
        self.nfft = int(self.DataSize/2)
        
        self.freqs = np.fft.fftfreq( n=self.DataSize, d=dt)
        Fourier = np.fft.fft(dataFFT)
        self.Magnitude = np.abs(Fourier)/self.nfft
        
        mean_acceleration   = Fourier[0].real/self.DataSize     # mG
        total_acceleration  = Fourier[0].real * 9.8 * 1e-3 * dt # m/s
        print('The sampling rate is ','{:10.4f}'.format(self.SamplingRate),'Hz')
        print('Mean value at FFT 0Hz:')
        print('{:10.4f}'.format(mean_acceleration),'mG')
        print('Total Acceleration:')
        print('{:10.4f}'.format(total_acceleration*3.6),'km/hr')



    def EnergyAnalysis(self):
        # energy loss approximation
        EnergyLoss = 0.0
        for i in range(1, self.nfft):
            freq = self.freqs[i]
            Mag = self.Magnitude[i]
            EnergyLoss += Mag * Mag / (freq * freq) 
        print('Reduced energy loss = ',EnergyLoss,'μ G^2 s^2')

    
    def MaxMagnitude(self):    
        print('Maximum Magnitude & the corresponding frequencies')
        self.SortedIndex = np.argsort(self.Magnitude[1:self.nfft])
        Nmax = 8
        self.max_mag_freq_list = []
        for i in range(Nmax):
            idx = -i-1
            SortedIdx = self.SortedIndex[idx]+1
            frequency = self.freqs[SortedIdx]
            print( '{:10.4f}'.format(self.Magnitude[SortedIdx]),
                    'mG at',
                    '{:10.4f}'.format(self.freqs[SortedIdx]),
                    'Hz' 
                    )
            self.max_mag_freq_list.append
            
        
