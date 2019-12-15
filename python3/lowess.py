# import numpy as np
# import pylab as plt
# import statsmodels.api as sm
#
# x = np.linspace(0,2*np.pi,100)
# y = np.sin(x) + np.random.random(100) * 0.2
# lowess = sm.nonparametric.lowess(y, x, frac=0.1)
#
# plt.plot(x, y, '+')
# plt.plot(lowess[:, 0], lowess[:, 1])
# plt.show()

import numpy
def smooth(x,window_len=11,window='hanning'):
        if x.ndim != 1:
            raise ValueError("smooth only accepts 1 dimension arrays.")
        if x.size < window_len:
            raise ValueError("Input vector needs to be bigger than window size.")
        if window_len<3:
                return x
        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
                raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")
        s=numpy.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
        if window == 'flat': #moving average
                w=numpy.ones(window_len,'d')
        else:
                w=eval('numpy.'+window+'(window_len)')
        y=numpy.convolve(w/w.sum(),s,mode='same')
        return y[window_len:-window_len+1]


a = numpy.array([x[1] for x in results])
smoothed = smooth(a,window_len=21)
results = zip([x[0] for x in results], smoothed)
