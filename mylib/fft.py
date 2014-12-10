# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 09:33:50 2014

@author: ffontana
"""
import numpy as np
def fft(t, y):
    dt = np.mean(np.diff(t))
    
    NFFT=t.size
    fft =abs(np.fft.fft(y, NFFT)/NFFT )

    fft = fft[0:NFFT/2] # take only right hand side (positive frequencies)
    fft[1:] = 2*fft[1:] # take into account that we only take the right hand side

    freq = np.fft.fftfreq(NFFT, dt)
    freq = freq[0:NFFT/2]
    return (freq, fft)