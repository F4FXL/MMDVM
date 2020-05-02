# Losely based on https://github.com/gnuradio/gnuradio/blob/master/gr-analog/python/analog/fm_emph.py

import numpy as np
import scipy.signal as signal
import pylab as pl
import math    
import cmath

fs = 24000
tau = 750e-6
ftau = 1/(2*np.pi * tau)
fch = 2700
maxGaindB=2
deemphasis = False #change to false for deemphasis

g = np.power(10, maxGaindB / 20)
w_cl = 1.0 / tau
w_ch = 2.0 * math.pi * fch

# Prewarped analog corner frequencies
w_cla = 2.0 * fs * math.tan(w_cl / (2.0 * fs))
w_cha = 2.0 * fs * math.tan(w_ch / (2.0 * fs))

# Resulting digital pole, zero, and gain term from the bilinear
# transformation of H(s) = (s + w_cla) / (s + w_cha) to
# H(z) = b0 (1 - z1 z^-1)/(1 - p1 z^-1)
kl = -w_cla / (2.0 * fs)
kh = -w_cha / (2.0 * fs)
z1 = (1.0 + kl) / (1.0 - kl)
p1 = (1.0 + kh) / (1.0 - kh)
b0 = (1.0 - kl) / (1.0 - kh)

btaps = [ b0 * 1.0, b0 * -z1, 0 ]
ataps = [      1.0,      -p1, 0 ]

f,h = signal.freqz(btaps,ataps, worN=[fs/2], fs=fs)
g = np.abs(h[0] * g)

btaps = [ g * b0 * 1.0, g * b0 * -z1, 0 ]
ataps = [      1.0,      -p1, 0 ]

if deemphasis: #deemphasis TF is the inverse function of preemphasis, so just swap coeffs
    temp  = btaps
    btaps = ataps
    ataps = temp

# f,h = signal.freqz(btaps,ataps, worN=[fs/2], fs=fs)
# print("Gain")
# print(20*np.log10(np.abs(h)))

taps = np.concatenate((btaps, ataps), axis=0)
print("Taps")
print(*taps, ",", sep="", end="\n")

print("-------------------------")
print("Q15")
print("Taps")
print(*np.round(np.array(taps) * (2**15)).astype(int), "", sep=",", end="\n")

f,h = signal.freqz(btaps,ataps, fs=fs)
pl.plot(f, 20*np.log10(np.abs(h)))
pl.xlabel('frequency/Hz')
pl.ylabel('gain/dB')
pl.ylim(top=15,bottom=-15)
pl.xlim(left=0, right=fch*2.5)

pl.show()