import numpy as np
import scipy.signal as signal
import pylab as pl
import math

fs = 48000
tau = 750e-6

w_p = 1/tau
w_pp = math.tan (w_p / (fs * 2)) # prewarped analog freq

a0 = 1
a1 = (w_pp - 1)/(w_pp + 1)
a2 = 0

b0 = w_pp/(1 + w_pp)
b1 = b0
b2 = 0

btaps = [b0, b1, b2]
ataps = [a0, a1, a2]

print(btaps)
print(ataps)

z,p,k = signal.tf2zpk(btaps, ataps)
print(20*math.log10(k))

f,h = signal.freqz(btaps,ataps, fs=fs)
pl.plot(f,20*np.log10(np.abs(h)))
pl.xlabel('frequency/Hz');
pl.ylabel('gain/dB');
pl.ylim(top=1,bottom=-20);
pl.xlim(left=0, right=2700);
pl.show()
